from flask import Flask, request, session, redirect, url_for, render_template_string, jsonify
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


DB_PATH = os.path.join(os.path.dirname(__file__), "auth_users.db")
SECRET = os.environ.get("APP_SECRET_KEY", "dev-secret-change-me")


def get_conn():
		conn = sqlite3.connect(DB_PATH)
		conn.row_factory = sqlite3.Row
		return conn


def ensure_schema():
		conn = get_conn()
		cur = conn.cursor()
		cur.execute(
				"""
				CREATE TABLE IF NOT EXISTS users (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						username TEXT NOT NULL UNIQUE,
						password_hash TEXT NOT NULL
				)
				"""
		)
		conn.commit()
		conn.close()


app = Flask(__name__)
app.secret_key = SECRET


BASE = """
<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>{{ title or 'Auth Demo' }}</title>
	</head>
	<body>
		<nav>
			{% if session.get('user') %}
				Logged in as <strong>{{ session.get('user') }}</strong>
				| <a href="{{ url_for('profile') }}">Profile</a>
				| <a href="{{ url_for('logout') }}">Logout</a>
			{% else %}
				<a href="{{ url_for('register') }}">Register</a>
				| <a href="{{ url_for('login') }}">Login</a>
			{% endif %}
		</nav>
		<hr>
		{% block content %}{% endblock %}
	</body>
	</html>
"""


REGISTER = """
{% extends base %}
{% block content %}
	<h1>Create an account</h1>
	{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
	<form method="post">
		<label>Username <input name="username" value="{{ request.form.get('username','') }}"></label><br>
		<label>Password <input name="password" type="password"></label><br>
		<button type="submit">Register</button>
	</form>
{% endblock %}
"""


LOGIN = """
{% extends base %}
{% block content %}
	<h1>Login</h1>
	{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
	<form method="post">
		<label>Username <input name="username" value="{{ request.form.get('username','') }}"></label><br>
		<label>Password <input name="password" type="password"></label><br>
		<button type="submit">Login</button>
	</form>
{% endblock %}
"""


PROFILE = """
{% extends base %}
{% block content %}
	<h1>Profile</h1>
	<p>Welcome, {{ session.get('user') }}.</p>
{% endblock %}
"""


def strong_enough(pw: str) -> bool:
		# Simple policy: at least 8 chars, includes digit and letter
		if len(pw) < 8:
				return False
		has_digit = any(c.isdigit() for c in pw)
		has_alpha = any(c.isalpha() for c in pw)
		return has_digit and has_alpha


@app.route("/")
def index():
		if session.get("user"):
				return redirect(url_for("profile"))
		return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
		ensure_schema()
		error = None
		if request.method == "POST":
				username = (request.form.get("username") or "").strip()
				password = request.form.get("password") or ""
				if not username or not password:
						error = "Username and password required"
				elif not strong_enough(password):
						error = "Password must be 8+ chars with letters and numbers"
				else:
						phash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
						conn = get_conn()
						try:
								conn.execute(
										"INSERT INTO users (username, password_hash) VALUES (?, ?)",
										(username, phash),
								)
								conn.commit()
								session["user"] = username
								return redirect(url_for("profile"))
						except sqlite3.IntegrityError:
								error = "Username already exists"
						finally:
								conn.close()
		return render_template_string(REGISTER, base=BASE, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
		ensure_schema()
		error = None
		if request.method == "POST":
				username = (request.form.get("username") or "").strip()
				password = request.form.get("password") or ""
				conn = get_conn()
				row = conn.execute("SELECT id, username, password_hash FROM users WHERE username=?", (username,)).fetchone()
				conn.close()
				if not row or not check_password_hash(row["password_hash"], password):
						error = "Invalid username or password"
				else:
						session["user"] = row["username"]
						return redirect(url_for("profile"))
		return render_template_string(LOGIN, base=BASE, error=error)


@app.route("/logout")
def logout():
		session.clear()
		return redirect(url_for("login"))


@app.get("/api/me")
def api_me():
		if not session.get("user"):
				return jsonify({"error": "unauthorized"}), 401
		return jsonify({"username": session["user"]})


if __name__ == "__main__":
		ensure_schema()
		app.run(debug=True, port=5011)

