from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder="user_specific_templates")
app.secret_key = "userdevsecretchangeme"  # Change this in production
DB_PATH = os.path.join(os.path.dirname(__file__), "users_specific.db")

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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY (owner_id) REFERENCES accounts(id)
        )
        """
    )
    conn.commit()
    conn.close()


def simple_hash(pw: str) -> str:
    salt = "slt"
    h = 0x811C9DC5
    for ch in (salt + pw):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def find_user_by_username(username: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, password_hash FROM accounts WHERE lower(username)=lower(?)", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def create_user(username: str, email: str, password: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (username, email, password_hash, created_at) VALUES (?,?,?,?)",
                (username, email, simple_hash(password), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def update_last_login(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET last_login=? WHERE id=?", (datetime.utcnow().isoformat(), user_id))
    conn.commit()
    conn.close()


def login_required(view):
    from functools import wraps
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


def own_item_required(item_id):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    conn.close()
    if not row:
        return None
    if row["owner_id"] != session.get("user_id"):
        return False
    return row


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
                update_last_login(user_id)
                flash("Logged in.", "success")
                return redirect(url_for("my_items"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("home"))


@app.route("/items")
@login_required
def my_items():
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM items WHERE owner_id=? ORDER BY datetime(created_at) DESC", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("items.html", items=rows)


@app.route("/items/create", methods=["GET", "POST"])
@login_required
def create_item():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        body = (request.form.get("body") or "").strip()
        if not title or not body:
            flash("Title and body required.", "error")
            return render_template("item_form.html", mode="create", item=None)
        conn = get_conn()
        conn.execute("INSERT INTO items (owner_id, title, body, created_at) VALUES (?,?,?,?)",
                     (session["user_id"], title, body, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        flash("Item created.", "success")
        return redirect(url_for("my_items"))
    return render_template("item_form.html", mode="create", item=None)


@app.route("/items/<int:item_id>")
@login_required
def view_item(item_id):
    row = own_item_required(item_id)
    if row is None:
        flash("Item not found.", "error")
        return redirect(url_for("my_items"))
    if row is False:
        flash("Not allowed.", "error")
        return redirect(url_for("my_items"))
    return render_template("item_view.html", item=row)


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    row = own_item_required(item_id)
    if row is None:
        flash("Item not found.", "error")
        return redirect(url_for("my_items"))
    if row is False:
        flash("Not allowed.", "error")
        return redirect(url_for("my_items"))
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        body = (request.form.get("body") or "").strip()
        if not title or not body:
            flash("Title and body required.", "error")
            return render_template("item_form.html", mode="edit", item=row)
        conn = get_conn()
        conn.execute("UPDATE items SET title=?, body=?, updated_at=? WHERE id=?",
                     (title, body, datetime.utcnow().isoformat(), item_id))
        conn.commit()
        conn.close()
        flash("Item updated.", "success")
        return redirect(url_for("view_item", item_id=item_id))
    return render_template("item_form.html", mode="edit", item=row)


@app.route("/items/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    row = own_item_required(item_id)
    if row is None:
        flash("Item not found.", "error")
        return redirect(url_for("my_items"))
    if row is False:
        flash("Not allowed.", "error")
        return redirect(url_for("my_items"))
    conn = get_conn()
    conn.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    flash("Item deleted.", "success")
    return redirect(url_for("my_items"))

if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)

