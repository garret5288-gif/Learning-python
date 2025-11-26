from flask import Flask, request, render_template_string, redirect, url_for, make_response
import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "xss_messages.db")


def get_conn():
		conn = sqlite3.connect(DB_PATH)
		conn.row_factory = sqlite3.Row
		return conn


def ensure_schema():
		conn = get_conn()
		cur = conn.cursor()
		cur.execute(
				"""
				CREATE TABLE IF NOT EXISTS messages (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						author TEXT NOT NULL,
						content TEXT NOT NULL,
						created_at TEXT NOT NULL
				)
				"""
		)
		conn.commit()
		conn.close()


app = Flask(__name__)


HTML = """
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>XSS-Safe Board</title>
	</head>
	<body>
		<h1>XSS-Safe Message Board</h1>
		<p>Notes:</p>
		<ul>
			<li>Templates auto-escape by default (Jinja2). We do not use the |safe filter on user content.</li>
			<li>Security headers (CSP, X-Content-Type-Options, X-Frame-Options) are applied.</li>
			<li>User input is treated as plain text; any HTML tags are displayed literally.</li>
		</ul>
		<form method="post" action="/post">
			<input name="author" placeholder="Your name" value="{{ request.form.get('author','') }}">
			<br>
			<textarea name="content" rows="4" cols="40" placeholder="Write a message...">{{ request.form.get('content','') }}</textarea>
			<br>
			<button type="submit">Post</button>
		</form>
		<hr>
		{% if rows %}
			<h2>Messages</h2>
			<ul>
			{% for r in rows %}
				<li>
					<strong>{{ r['author'] }}</strong> at {{ r['created_at'] }}<br>
					{{ r['content'] }}
				</li>
			{% endfor %}
			</ul>
		{% else %}
			<p>No messages yet.</p>
		{% endif %}
		<p><small>Try submitting &lt;script&gt;alert(1)&lt;/script&gt; — it will be rendered harmlessly as text.</small></p>
	</body>
	</html>
"""


def apply_security_headers(resp):
		# Content Security Policy: no inline scripts, no external scripts/styles
		csp = "default-src 'self'; script-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
		resp.headers['Content-Security-Policy'] = csp
		resp.headers['X-Content-Type-Options'] = 'nosniff'
		resp.headers['X-Frame-Options'] = 'DENY'
		return resp


@app.after_request
def _after(resp):
		return apply_security_headers(resp)


@app.get("/")
def home():
		ensure_schema()
		conn = get_conn()
		rows = conn.execute("SELECT id, author, content, created_at FROM messages ORDER BY id DESC LIMIT 100").fetchall()
		conn.close()
		return render_template_string(HTML, rows=rows)


@app.post("/post")
def post_msg():
		ensure_schema()
		author = (request.form.get("author") or "Anonymous").strip() or "Anonymous"
		content = (request.form.get("content") or "").strip()
		if not content:
				# Re-render with a minimal warning; do not reflect raw content unsafely
				conn = get_conn()
				rows = conn.execute("SELECT id, author, content, created_at FROM messages ORDER BY id DESC LIMIT 100").fetchall()
				conn.close()
				resp = make_response(render_template_string(HTML, rows=rows))
				return resp
		conn = get_conn()
		conn.execute(
				"INSERT INTO messages (author, content, created_at) VALUES (?, ?, ?)",
				(author, content, datetime.utcnow().isoformat()),
		)
		conn.commit()
		conn.close()
		return redirect(url_for("home"))


if __name__ == "__main__":
		ensure_schema()
		app.run(debug=True, port=5012)

