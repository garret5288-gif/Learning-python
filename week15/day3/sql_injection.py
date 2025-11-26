from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "safe_users.db")


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
						email TEXT NOT NULL,
						role TEXT NOT NULL
				)
				"""
		)
		conn.commit()
		# seed
		cur.execute("SELECT COUNT(*) FROM users")
		if cur.fetchone()[0] == 0:
				cur.executemany(
						"INSERT INTO users (username, email, role) VALUES (?, ?, ?)",
						[
								("alice", "alice@example.com", "admin"),
								("bob", "bob@example.com", "user"),
								("carol", "carol@example.com", "user"),
								("dave", "dave@example.com", "moderator"),
						],
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
		<title>Safe User Search</title>
	</head>
	<body>
		<h1>Safe User Search</h1>
		<form method="get" action="/">
			<input type="text" name="q" value="{{ q }}" placeholder="username contains...">
			<select name="sort">
				<option value="username" {% if sort=='username' %}selected{% endif %}>Username</option>
				<option value="email" {% if sort=='email' %}selected{% endif %}>Email</option>
				<option value="role" {% if sort=='role' %}selected{% endif %}>Role</option>
			</select>
			<select name="dir">
				<option value="asc" {% if dir=='asc' %}selected{% endif %}>Asc</option>
				<option value="desc" {% if dir=='desc' %}selected{% endif %}>Desc</option>
			</select>
			<button type="submit">Search</button>
		</form>
		{% if rows %}
			<p>Found {{ rows|length }} result(s)</p>
			<table border="1" cellpadding="6">
				<thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr></thead>
				<tbody>
					{% for r in rows %}
					<tr>
						<td>{{ r['id'] }}</td>
						<td>{{ r['username'] }}</td>
						<td>{{ r['email'] }}</td>
						<td>{{ r['role'] }}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table>
		{% else %}
			<p>No results.</p>
		{% endif %}
		<p><small>Protection: parameterized queries for filters, allow-listed columns for sort, and limited direction.</small></p>
	</body>
	</html>
"""


ALLOWED_SORTS = {"username": "username", "email": "email", "role": "role"}
ALLOWED_DIRS = {"asc": "ASC", "desc": "DESC"}


@app.route("/")
def home():
		ensure_schema()
		q = (request.args.get("q") or "").strip()
		sort = request.args.get("sort") or "username"
		direction = request.args.get("dir") or "asc"
		sort_col = ALLOWED_SORTS.get(sort, "username")
		sort_dir = ALLOWED_DIRS.get(direction.lower(), "ASC")

		sql = f"SELECT id, username, email, role FROM users"
		params = []
		if q:
				sql += " WHERE username LIKE ?"
				params.append(f"%{q}%")
		sql += f" ORDER BY {sort_col} {sort_dir}"
		sql += " LIMIT 100"

		conn = get_conn()
		rows = conn.execute(sql, params).fetchall()
		conn.close()
		return render_template_string(HTML, rows=rows, q=q, sort=sort, dir=direction)


@app.get("/api/users")
def api_users():
		ensure_schema()
		q = (request.args.get("q") or "").strip()
		sql = "SELECT id, username, email, role FROM users"
		params = []
		if q:
				sql += " WHERE username LIKE ?"
				params.append(f"%{q}%")
		sql += " ORDER BY username ASC LIMIT 100"
		conn = get_conn()
		rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
		conn.close()
		return jsonify(rows)


@app.post("/api/users")
def api_create_user():
		ensure_schema()
		data = request.get_json(silent=True) or {}
		username = (data.get("username") or "").strip()
		email = (data.get("email") or "").strip()
		role = (data.get("role") or "user").strip() or "user"
		if not username or not email:
				return jsonify({"error": "username and email required"}), 400
		conn = get_conn()
		try:
				conn.execute(
						"INSERT INTO users (username, email, role) VALUES (?, ?, ?)",
						(username, email, role),
				)
				conn.commit()
		except sqlite3.IntegrityError:
				conn.close()
				return jsonify({"error": "username already exists"}), 409
		row = conn.execute("SELECT id, username, email, role FROM users WHERE username=?", (username,)).fetchone()
		conn.close()
		return jsonify(dict(row)), 201


if __name__ == "__main__":
		ensure_schema()
		app.run(debug=True, port=5010)

