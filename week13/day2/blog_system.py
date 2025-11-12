import os
import sqlite3
from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
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
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        author = (request.form.get("author") or "").strip() or "Anonymous"

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

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        content = (request.form.get("content") or "").strip()
        author = (request.form.get("author") or "").strip() or post["author"]

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
    delete_post(post["id"])
    flash("Post deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)



