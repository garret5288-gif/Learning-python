from flask import Flask, render_template, request, flash
import sqlite3
from flask import session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__, template_folder="protected_admin_templates")
app.secret_key = "protectedadminsecretchangeme"  # Change this in production
DB_PATH = os.path.join(os.path.dirname(__file__), "users_protected_admin.db")
ADMIN_KEY = "adminsecretkeychangeme"  # Change this in production


def get_conn():
    return sqlite3.connect(DB_PATH)


def ensure_schema():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def admin_required(view):
    from functools import wraps

    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin login required.", "error")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    ensure_schema()
    if request.method == "POST":
        key = (request.form.get("key") or "").strip()
        if key == ADMIN_KEY:
            session["is_admin"] = True
            flash("Admin session started.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid admin key.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout", methods=["POST"]) 
@admin_required
def admin_logout():
    session.pop("is_admin", None)
    flash("Admin session ended.", "success")
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    return render_template("admin_dashboard.html")


def list_users():
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM users ORDER BY lower(username)").fetchall()
    conn.close()
    return rows


def create_user(username, email):
    conn = get_conn()
    conn.execute(
        "INSERT INTO users (username, email, created_at) VALUES (?,?,?)",
        (username, email, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_conn()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


@app.route("/admin/users")
@admin_required
def admin_users():
    rows = list_users()
    return render_template("admin_users.html", users=rows)


@app.route("/admin/users/add", methods=["GET", "POST"])
@admin_required
def admin_add_user():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        if not username or not email:
            flash("Username and email required.", "error")
            return render_template("admin_user_form.html")
        try:
            create_user(username, email)
            flash("User added.", "success")
            return redirect(url_for("admin_users"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
    return render_template("admin_user_form.html")


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    delete_user(user_id)
    flash("User deleted.", "success")
    return redirect(url_for("admin_users"))


if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)

