import sqlite3
import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for, flash

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

app = Flask(__name__, template_folder="user_templates")
app.secret_key = "dev-secret-change-me"  

def get_conn():
    return sqlite3.connect(DB_PATH)

def ensure_schema():
    conn = get_conn()
    cur = conn.cursor()
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
    conn.commit()
    conn.close()

def hash_password(pw: str) -> str:
    """Very simple non-cryptographic hash (for learning only)."""
    salt = "slt"  # static demo salt
    h = 0x811C9DC5
    for ch in (salt + pw):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF  # 32-bit wrap
    return f"{h:08x}"

def find_user_by_username(username: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, password_hash, created_at, last_login FROM accounts WHERE lower(username)=lower(?)", (username,))
    row = cur.fetchone()
    conn.close()
    return row

def create_user(username: str, email: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)", (
        username.strip(), email.strip(), hash_password(password), datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def update_last_login(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET last_login=? WHERE id=?", (datetime.utcnow().isoformat(), user_id))
    conn.commit()
    conn.close()

def is_logged_in() -> bool:
    return "user_id" in session

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            flash("Please login first.")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        pw = request.form.get("password", "")
        pw2 = request.form.get("confirm_password", "")
        if not username or not email or not pw:
            flash("All fields are required.")
        elif pw != pw2:
            flash("Passwords do not match.")
        elif find_user_by_username(username):
            flash("Username already taken.")
        else:
            try:
                create_user(username, email, pw)
                flash("Registration successful. Please login.")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Email already in use.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        pw = request.form.get("password", "")
        row = find_user_by_username(username)
        if not row:
            flash("Invalid credentials.")
        else:
            user_id, uname, email, password_hash, created_at, last_login = row
            if hash_password(pw) != password_hash:
                flash("Invalid credentials.")
            else:
                session["user_id"] = user_id
                session["username"] = uname
                update_last_login(user_id)
                flash("Logged in.")
                return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session.get("username"))

@app.route("/users")
@login_required
def list_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, email, created_at, last_login FROM accounts ORDER BY lower(username)")
    rows = cur.fetchall()
    conn.close()
    return render_template("users.html", rows=rows)

def init():
    ensure_schema()

if __name__ == "__main__":
    init()
    app.run(debug=True)


