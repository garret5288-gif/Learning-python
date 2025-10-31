from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import requests
import os
import csv
import time

APP_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(APP_DIR, "cs50_templates")
DB_PATH = os.path.join(APP_DIR, "finance.db")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=TEMPLATES_DIR)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")


# ---------- Utilities ----------
def get_db(): # Get a database connection
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db(): # Initialize the database with required tables
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"""
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			hash TEXT NOT NULL,
			cash REAL NOT NULL DEFAULT 10000
		);
		"""
	)
	cur.execute( # Create transactions table
		"""
		CREATE TABLE IF NOT EXISTS transactions (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL,
			symbol TEXT NOT NULL,
			shares INTEGER NOT NULL,
			price REAL NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY(user_id) REFERENCES users(id)
		);
		"""
	)
	conn.commit()
	conn.close()


def login_required(f): # Decorator to require login for routes
	@wraps(f)
	def decorated(*args, **kwargs):
		if session.get("user_id") is None:
			return redirect(url_for("login"))
		return f(*args, **kwargs)
	return decorated


def apology(message, code=400): # Render apology message
	return render_template("apology.html", message=message, code=code), code


def lookup(symbol: str): # Lookup stock symbol
	"""Fetch a simple quote for a stock symbol using Stooq CSV; fallback to static prices."""
	if not symbol:
		return None
	sym = symbol.strip().lower()
	# Try Stooq (no API key)
	try:
		url = f"https://stooq.com/q/l/?s={sym}&f=sd2t2ohlcv&h&e=csv"
		r = requests.get(url, timeout=6)
		if r.status_code == 200 and r.text:
			rows = list(csv.DictReader(r.text.splitlines()))
			if rows:
				row = rows[0]
				# Stooq returns 'N/D' for missing
				if row.get("Close") and row["Close"].upper() != "N/D":
					price = float(row["Close"]) if row["Close"] else None
					name = (row.get("Symbol") or sym).upper()
					if price:
						return {"symbol": name, "price": round(price, 2)}
	except requests.RequestException:
		pass

	# Fallback static mapping
	static = { 
		"AAPL": 175.00,
		"MSFT": 330.00,
		"GOOG": 140.00,
		"AMZN": 125.00,
	}
	up = sym.upper()
	if up in static:
		return {"symbol": up, "price": static[up]}
	return None


# Ensure DB exists on import
os.makedirs(TEMPLATES_DIR, exist_ok=True)
init_db()


# ---------- Routes ----------
@app.route("/")
@login_required
def index():
	user_id = session["user_id"]
	conn = get_db()
	cur = conn.cursor()

	# Aggregate holdings from transactions
	cur.execute(
		"""
		SELECT symbol, SUM(shares) AS total_shares
		FROM transactions
		WHERE user_id = ?
		GROUP BY symbol
		HAVING total_shares <> 0
		ORDER BY symbol
		""",
		(user_id,),
	)
	rows = cur.fetchall()

	portfolio = []
	total_value = 0.0
	for row in rows:
		symbol = row["symbol"].upper()
		shares = int(row["total_shares"]) if row["total_shares"] else 0
		q = lookup(symbol)
		price = q["price"] if q else 0.0
		value = round(shares * price, 2)
		total_value += value
		portfolio.append({"symbol": symbol, "shares": shares, "price": price, "value": value})

	cur.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
	cash = cur.fetchone()["cash"]
	conn.close()

	grand_total = round(total_value + cash, 2)
	return render_template("index.html", portfolio=portfolio, cash=round(cash, 2), total=round(total_value, 2), grand_total=grand_total)


@app.route("/register", methods=["GET", "POST"])
def register(): # User registration
	if request.method == "GET":
		return render_template("register.html")

	username = (request.form.get("username") or "").strip()
	password = request.form.get("password") or ""
	confirmation = request.form.get("confirmation") or ""

	if not username or not password or not confirmation:
		return apology("missing credentials")
	if password != confirmation:
		return apology("passwords must match")

	hash_ = generate_password_hash(password)
	try: # Insert new user
		conn = get_db()
		cur = conn.cursor()
		cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_))
		conn.commit()
		user_id = cur.lastrowid
		conn.close()
	except sqlite3.IntegrityError:
		return apology("username taken")

	session["user_id"] = user_id
	return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login(): # User login
	session.clear()
	if request.method == "GET":
		return render_template("login.html")

	username = (request.form.get("username") or "").strip()
	password = request.form.get("password") or ""
	if not username or not password:
		return apology("missing credentials")

	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT id, hash FROM users WHERE username = ?", (username,))
	row = cur.fetchone()
	conn.close()

	if not row or not check_password_hash(row["hash"], password):
		return apology("invalid username/password")

	session["user_id"] = row["id"]
	return redirect(url_for("index"))


@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote(): # Get stock quote
	if request.method == "GET":
		return render_template("quote.html")
	symbol = (request.form.get("symbol") or "").strip().upper()
	q = lookup(symbol)
	if not q:
		return apology("invalid symbol")
	return render_template("quoted.html", quote=q)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy(): # Buy stocks
	if request.method == "GET":
		return render_template("buy.html")

	symbol = (request.form.get("symbol") or "").strip().upper()
	shares_raw = request.form.get("shares") or ""
	if not symbol or not shares_raw.isdigit():
		return apology("invalid input")
	shares = int(shares_raw)
	if shares <= 0: # Ensure shares are positive
		return apology("shares must be positive")

	q = lookup(symbol)
	if not q:
		return apology("invalid symbol")
	price = q["price"]

	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
	cash = cur.fetchone()["cash"]
	cost = round(price * shares, 2)
	if cost > cash:
		conn.close()
		return apology("can't afford")

	# Record transaction and update cash
	cur.execute( # Insert new transaction
		"INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
		(session["user_id"], symbol, shares, price),
	)
	cur.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cost, session["user_id"]))
	conn.commit()
	conn.close()
	return redirect(url_for("index"))


@app.route("/sell", methods=["GET", "POST"]) # Sell stocks
@login_required
def sell():
	conn = get_db()
	cur = conn.cursor()
	# symbols owned
	cur.execute(
		"""
		SELECT symbol, SUM(shares) AS total_shares
		FROM transactions
		WHERE user_id = ?
		GROUP BY symbol
		HAVING total_shares > 0
		ORDER BY symbol
		""",
		(session["user_id"],),
	)
	owned = cur.fetchall() # list of rows with symbol and total_shares

	if request.method == "GET":
		conn.close()
		return render_template("sell.html", owned=owned)

	symbol = (request.form.get("symbol") or "").strip().upper()
	shares_raw = request.form.get("shares") or ""
	if not symbol or not shares_raw.isdigit():
		conn.close()
		return apology("invalid input")
	shares = int(shares_raw)
	if shares <= 0:
		conn.close()
		return apology("shares must be positive")

	# Check ownership
	cur.execute(
		"SELECT COALESCE(SUM(shares),0) as total FROM transactions WHERE user_id=? AND symbol=?",
		(session["user_id"], symbol),
	)
	total_owned = cur.fetchone()["total"]
	if shares > total_owned:
		conn.close()
		return apology("too many shares")

	q = lookup(symbol) # Get current price
	if not q:
		conn.close()
		return apology("invalid symbol")
	price = q["price"]
	proceeds = round(price * shares, 2)

	# Record negative shares and add cash
	cur.execute(
		"INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
		(session["user_id"], symbol, -shares, price),
	)
	cur.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (proceeds, session["user_id"]))
	conn.commit()
	conn.close()
	return redirect(url_for("index"))


@app.route("/history")
@login_required
def history():
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"""
		SELECT symbol, shares, price, created_at
		FROM transactions
		WHERE user_id = ?
		ORDER BY created_at DESC, id DESC
		""",
		(session["user_id"],),
	)
	rows = cur.fetchall()
	conn.close()
	return render_template("history.html", rows=rows)


if __name__ == "__main__":
	app.run(debug=True)

