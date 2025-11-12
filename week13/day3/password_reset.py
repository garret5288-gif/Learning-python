import os
import sqlite3
import secrets
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__, template_folder="password_templates")
app.secret_key = "anotherdevsecretchangeme"  # Change this in production
DB_PATH = os.path.join(os.path.dirname(__file__), "users_reset.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def simple_hash(pw: str) -> str:
    # Very simple educational hash (not secure)
    salt = "slt"
    h = 0x811C9DC5
    for ch in (salt + pw):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def ensure_schema():
    conn = get_conn()
    cur = conn.cursor()
    # accounts table for registration/login
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login TEXT
        )
        """
    )
    # reset tokens
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reset_token TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            used INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES accounts(id)
        )
        """
    )
    conn.commit()
    conn.close()


def find_user_by_username(username: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, password_hash FROM accounts WHERE lower(username)=lower(?)",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def create_user(username: str, email: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO accounts (username, email, password_hash, created_at) VALUES (?,?,?,?)",
        (username, email, simple_hash(password), datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def update_password(user_id: int, new_password: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE accounts SET password_hash=? WHERE id=?",
        (simple_hash(new_password), user_id),
    )
    conn.commit()
    conn.close()


def create_reset_token(user_id: int, token: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO password_resets (user_id, reset_token, created_at) VALUES (?, ?, datetime('now'))",
        (user_id, token),
    )
    conn.commit()
    conn.close()


def validate_reset_token(token: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id FROM password_resets WHERE reset_token=? AND used=0",
        (token,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def mark_token_used(token_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE password_resets SET used=1 WHERE id=?", (token_id,))
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        pw = request.form.get("password") or ""
        pw2 = request.form.get("confirm_password") or ""
        if not username or not email or not pw:
            flash("All fields are required.", "error")
        elif pw != pw2:
            flash("Passwords do not match.", "error")
        elif find_user_by_username(username):
            flash("Username already taken.", "error")
        else:
            try:
                create_user(username, email, pw)
                flash("Registration successful. Please login.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Email already in use.", "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        pw = request.form.get("password") or ""
        row = find_user_by_username(username)
        if not row:
            flash("Invalid credentials.", "error")
        else:
            user_id, uname, email, pw_hash = row
            if simple_hash(pw) != pw_hash:
                flash("Invalid credentials.", "error")
            else:
                session["user_id"] = user_id
                session["username"] = uname
                flash("Logged in.", "success")
                return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session.get("username"))


@app.route("/request-reset", methods=["GET", "POST"])
def request_reset():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        row = find_user_by_username(username)
        if not row:
            flash("If the account exists, a reset link will be shown.", "success")
            return redirect(url_for("login"))
        user_id = row[0]
        token = secrets.token_urlsafe(24)
        create_reset_token(user_id, token)
        # Dev-only: show the reset link directly
        flash(f"Reset link: {url_for('reset_password', token=token, _external=False)}", "success")
        return redirect(url_for("login"))
    return render_template("request_reset.html")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    token_data = validate_reset_token(token)
    if not token_data:
        flash("Invalid or used reset token.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        new_password = (request.form.get("password") or "").strip()
        confirm = (request.form.get("confirm_password") or "").strip()
        if not new_password:
            flash("Password required.", "error")
        elif new_password != confirm:
            flash("Passwords do not match.", "error")
        else:
            token_id, user_id = token_data
            update_password(user_id, new_password)
            mark_token_used(token_id)
            flash("Password has been reset. Please login.", "success")
            return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)


if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)
