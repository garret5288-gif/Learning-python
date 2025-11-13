import os
import sqlite3
from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "blog.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            );
            """
        )


def list_posts():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY datetime(created_at) DESC"
        ).fetchall()
        return rows


def get_post(post_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        return row


def create_post(title: str, content: str, author: str) -> int:
    now = datetime.utcnow().isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO posts(title, content, author, created_at) VALUES(?,?,?,?)",
            (title, content, author, now),
        )
        conn.commit()
        return cur.lastrowid


def update_post(post_id: int, title: str, content: str, author: str) -> None:
    now = datetime.utcnow().isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE posts SET title=?, content=?, author=?, updated_at=? WHERE id=?",
            (title, content, author, now, post_id),
        )
        conn.commit()


def delete_post(post_id: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()


app = Flask(__name__, template_folder="blog_templates")
app.secret_key = "supersecretkey"


@app.route("/")
def index():
    ensure_schema()
    posts = list_posts()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def view_post(post_id: int):
    ensure_schema()
    post = get_post(post_id)
    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("index"))
    return render_template("view.html", post=post)


@app.route("/create", methods=["GET", "POST"])
def create():
    ensure_schema()
    if "user_id" not in session:
        flash("Please login to create a post.", "error")
        return redirect(url_for("login"))
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        # Prefer logged-in username for author; fall back to form field or Anonymous
        author = (
            session.get("username")
            or (request.form.get("author") or "").strip()
            or "Anonymous"
        )

        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template("form.html", mode="create", post=None)

        post_id = create_post(title, content, author)
        flash("Post created.", "success")
        return redirect(url_for("view_post", post_id=post_id))

    return render_template("form.html", mode="create", post=None)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id: int):
    ensure_schema()
    post = get_post(post_id)
    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("index"))

    # Require login and ownership
    if "user_id" not in session or session.get("username") != post["author"]:
        flash("You can only edit your own posts.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        # Do not allow changing the author; enforce current user as author
        author = session.get("username") or post["author"]

        if not title or not content:
            flash("Title and content are required.", "error")
            return render_template("form.html", mode="edit", post=post)

        update_post(post["id"], title, content, author)
        flash("Post updated.", "success")
        return redirect(url_for("view_post", post_id=post["id"]))

    return render_template("form.html", mode="edit", post=post)


@app.route("/delete/<int:post_id>", methods=["POST"])
def remove(post_id: int):
    ensure_schema()
    post = get_post(post_id)
    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("index"))
    # Require login and ownership
    if "user_id" not in session or session.get("username") != post["author"]:
        flash("You can only delete your own posts.", "error")
        return redirect(url_for("index"))
    delete_post(post["id"])
    flash("Post deleted.", "success")
    return redirect(url_for("index"))



# --- Auth helpers and routes ---

def simple_hash(pw: str) -> str:
    salt = "slt"
    h = 0x811C9DC5
    for ch in (salt + pw):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def find_user_by_username(username: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT id, username, email, password_hash FROM accounts WHERE lower(username)=lower(?)",
            (username,),
        )
        return cur.fetchone()


def create_user(username: str, email: str, password: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO accounts (username, email, password_hash, created_at) VALUES (?,?,?,?)",
            (username.strip(), email.strip(), simple_hash(password), datetime.utcnow().isoformat()),
        )
        conn.commit()


def update_last_login(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE accounts SET last_login=? WHERE id=?", (datetime.utcnow().isoformat(), user_id))
        conn.commit()


@app.route("/register", methods=["GET", "POST"])
def register():
    ensure_schema()
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
    ensure_schema()
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
                return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)




