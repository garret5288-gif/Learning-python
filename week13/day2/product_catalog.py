import os
import sqlite3
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)


APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "products.db")
ADMIN_KEY = "admin123"  # change if desired


def ensure_schema():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT
            );
            """
        )


def list_products():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM products ORDER BY datetime(created_at) DESC"
        ).fetchall()
        return rows


def get_product(product_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        return row


def create_product(name, description, price, stock=0):
    now = datetime.utcnow().isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO products(name, description, price, stock, created_at) VALUES(?,?,?,?,?)",
            (name, description, float(price), int(stock or 0), now),
        )
        conn.commit()
        return cur.lastrowid


def update_product(product_id, name, description, price, stock=None):
    now = datetime.utcnow().isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        if stock is None:
            conn.execute(
                "UPDATE products SET name=?, description=?, price=?, updated_at=? WHERE id=?",
                (name, description, float(price), now, product_id),
            )
        else:
            conn.execute(
                "UPDATE products SET name=?, description=?, price=?, stock=?, updated_at=? WHERE id=?",
                (name, description, float(price), int(stock), now, product_id),
            )
        conn.commit()


def remove_product(product_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()


def adjust_stock(product_id, delta):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT stock FROM products WHERE id=?", (product_id,)).fetchone()
        if not row:
            return False
        new_stock = max(0, (row["stock"] or 0) + int(delta))
        conn.execute("UPDATE products SET stock=?, updated_at=? WHERE id=?", (
            new_stock, datetime.utcnow().isoformat(timespec="seconds"), product_id
        ))
        conn.commit()
        return True


app = Flask(__name__, template_folder="product_templates")
app.secret_key = "anothersecretkey"


def admin_required(view_func):
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin login required.", "error")
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)
    # Keep function name for Flask
    wrapper.__name__ = getattr(view_func, "__name__", "wrapped")
    return wrapper


@app.route("/")
def catalog():
    ensure_schema()
    products = list_products()
    return render_template("catalog.html", products=products)


@app.route("/product/<int:product_id>")
def view_product(product_id: int):
    ensure_schema()
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("catalog"))
    return render_template("product.html", product=product)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    ensure_schema()
    if request.method == "POST":
        key = (request.form.get("key") or "").strip()
        if key == ADMIN_KEY:
            session["is_admin"] = True
            flash("Admin session started.", "success")
            return redirect(url_for("admin"))
        flash("Invalid admin key.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout", methods=["POST"]) 
@admin_required
def admin_logout():
    session.pop("is_admin", None)
    flash("Admin session ended.", "success")
    return redirect(url_for("catalog"))


@app.route("/admin")
@admin_required
def admin():
    ensure_schema()
    products = list_products()
    return render_template("admin_list.html", products=products)


@app.route("/add", methods=["GET", "POST"])
@admin_required
def add_product():
    ensure_schema()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()
        price = request.form.get("price")
        stock = request.form.get("stock")

        if not name or not description or not price:
            flash("Name, description, and price are required.", "error")
            return render_template("add_product.html")

        try:
            price = float(price)
            stock = int(stock or 0)
        except ValueError:
            flash("Invalid number format.", "error")
            return render_template("add_product.html")

        product_id = create_product(name, description, price, stock)
        flash("Product added.", "success")
        return redirect(url_for("view_product", product_id=product_id))

    return render_template("add_product.html")


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id: int):
    ensure_schema()
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("admin"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()
        price = request.form.get("price")
        stock = request.form.get("stock")

        if not name or not description or not price:
            flash("Name, description, and price are required.", "error")
            return render_template("edit_product.html", product=product)

        try:
            price = float(price)
            stock = int(stock or product["stock"]) if stock != "" else product["stock"]
        except ValueError:
            flash("Invalid number format.", "error")
            return render_template("edit_product.html", product=product)

        update_product(product_id, name, description, price, stock)
        flash("Product updated.", "success")
        return redirect(url_for("view_product", product_id=product_id))

    return render_template("edit_product.html", product=product)


@app.route("/delete/<int:product_id>", methods=["POST"])
@admin_required
def delete_product(product_id: int):
    ensure_schema()
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("admin"))
    remove_product(product_id)
    flash("Product deleted.", "success")
    return redirect(url_for("admin"))


@app.route("/stock/<int:product_id>", methods=["POST"])
@admin_required
def stock_adjust(product_id: int):
    ensure_schema()
    action = request.form.get("action")
    amount = request.form.get("amount")
    try:
        amount = int(amount or 1)
    except ValueError:
        amount = 1
    delta = amount if action == "inc" else -amount
    if not adjust_stock(product_id, delta):
        flash("Unable to adjust stock.", "error")
    else:
        flash("Stock updated.", "success")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)

