import sqlite3
import atexit
from datetime import datetime

conn = sqlite3.connect("sales.db")  # Connect to SQLite database (or create it)
cur = conn.cursor()  # Create a cursor object to interact with the database

# --- Core tables ---
cur.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

# --- Products API ---
def add_product(name: str, price: float, stock: int = 0) -> None:
    """Add a product, or if it already exists by name, increase its stock.

    Price is only used on initial creation; existing product price is preserved.
    """
    cur.execute('SELECT id FROM products WHERE name = ? LIMIT 1', (name.strip(),))
    row = cur.fetchone()
    if row:
        cur.execute('UPDATE products SET stock = stock + ? WHERE id = ?', (stock, row[0]))
    else:
        cur.execute('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', (name, price, stock))
    conn.commit()

def get_all_products() -> list[dict]:
    cur.execute('SELECT id, name, price, stock FROM products ORDER BY id')
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in cur.fetchall()]

def find_product_by_id(pid: int) -> dict | None:
    cur.execute('SELECT id, name, price, stock FROM products WHERE id = ?', (pid,))
    r = cur.fetchone()
    return {"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} if r else None

# --- Customers API ---
def add_customer(name: str, email: str) -> None:
    cur.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))
    conn.commit()

def get_all_customers() -> list[dict]:
    cur.execute('SELECT id, name, email FROM customers ORDER BY id')
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in cur.fetchall()]

def find_customer_by_email(email: str) -> dict | None:
    cur.execute('SELECT id, name, email FROM customers WHERE email = ?', (email,))
    r = cur.fetchone()
    return {"id": r[0], "name": r[1], "email": r[2]} if r else None

# --- Orders API ---
def create_order(customer_id: int, items: list[tuple[int, int]]) -> int:
    """Create an order.
    items: list of (product_id, quantity)
    Returns order_id. Decrements stock, snapshots unit_price.
    """
    cur.execute('INSERT INTO orders (customer_id) VALUES (?)', (customer_id,))
    order_id = cur.lastrowid
    for product_id, qty in items:
        cur.execute('SELECT price, stock FROM products WHERE id = ?', (product_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Product {product_id} not found")
        price, stock = row
        if qty <= 0:
            raise ValueError("Quantity must be > 0")
        if stock is not None and stock < qty:
            raise ValueError("Insufficient stock")
        cur.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                    (order_id, product_id, qty, price))
        cur.execute('UPDATE products SET stock = stock - ? WHERE id = ?', (qty, product_id))
    conn.commit()
    return order_id

def list_orders() -> list[dict]:
    cur.execute('''
        SELECT o.id, o.order_date, c.id, c.name, c.email,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0)
        FROM orders o
        JOIN customers c ON c.id = o.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.id
        GROUP BY o.id
        ORDER BY o.order_date DESC, o.id DESC
    ''')
    return [{
        "order_id": r[0],
        "order_date": r[1],
        "customer_id": r[2],
        "customer_name": r[3],
        "customer_email": r[4],
        "total": r[5],
    } for r in cur.fetchall()]

def get_order_items(order_id: int) -> list[dict]:
    cur.execute('''
        SELECT p.id, p.name, oi.quantity, oi.unit_price, (oi.quantity * oi.unit_price)
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        WHERE oi.order_id = ?
        ORDER BY oi.id
    ''', (order_id,))
    return [{
        "product_id": r[0],
        "product_name": r[1],
        "quantity": r[2],
        "unit_price": r[3],
        "line_total": r[4],
    } for r in cur.fetchall()]

# --- Reports ---
def report_sales_by_product() -> list[dict]:
    cur.execute('''
        SELECT p.id, p.name,
               COALESCE(SUM(oi.quantity), 0) as units,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) as revenue
        FROM products p
        LEFT JOIN order_items oi ON oi.product_id = p.id
        GROUP BY p.id
        ORDER BY revenue DESC, units DESC
    ''')
    return [{"product_id": r[0], "name": r[1], "units": r[2], "revenue": r[3]} for r in cur.fetchall()]

# (Sales-by-customer report removed by request)

# (Monthly report removed by request)

# --- Utilities / CLI helpers ---
def _prompt_non_empty(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty.\n")

def _prompt_float(prompt: str, min_value: float | None = None) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if min_value is not None and val < min_value:
                print(f"Enter a number >= {min_value}.\n"); continue
            return val
        except ValueError:
            print("Please enter a valid number (e.g., 12.34).\n")

def _prompt_int(prompt: str, min_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_value is not None and val < min_value:
                print(f"Enter an integer >= {min_value}.\n"); continue
            return val
        except ValueError:
            print("Please enter a whole number.\n")

def clear_all_data() -> None:
    cur.execute('DELETE FROM order_items')
    cur.execute('DELETE FROM orders')
    cur.execute('DELETE FROM customers')
    cur.execute('DELETE FROM products')
    conn.commit()

def close_connection() -> None:
    try:
        conn.close()
    except Exception:
        pass

# Always attempt to close the DB when the process exits
atexit.register(close_connection)

def menu() -> None:
    print("Sales System")
    print("1. Add Product")
    print("2. View Products")
    print("3. Add Customer")
    print("4. View Customers")
    print("5. Create Order")
    print("6. View Orders")
    print("7. Report: Sales by Product")
    print("8. Clear ALL Data")
    print("9. Exit")

def main():
    while True:
        menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            close_connection()
            print("\nGoodbye!")
            break
        if choice == "1":
            name = _prompt_non_empty("Product name: ")
            price = _prompt_float("Price (> 0): ", min_value=0.01)
            stock = _prompt_int("Stock (>= 0): ", min_value=0)
            add_product(name, price, stock)
            print("Product added.\n")
        elif choice == "2":
            products = get_all_products()
            if not products:
                print("No products.\n")
            else:
                for p in products:
                    print(p)
                print()
        elif choice == "3":
            name = _prompt_non_empty("Customer name: ")
            email = _prompt_non_empty("Customer email: ")
            try:
                add_customer(name, email)
                print("Customer added.\n")
            except sqlite3.IntegrityError:
                print("A customer with that email already exists.\n")
        elif choice == "4":
            customers = get_all_customers()
            if not customers:
                print("No customers.\n")
            else:
                for c in customers:
                    print(c)
                print()
        elif choice == "5":
            email = _prompt_non_empty("Customer email for order: ")
            cust = find_customer_by_email(email)
            if not cust:
                print("Customer not found.\n"); continue
            items: list[tuple[int, int]] = []
            while True:
                print("Enter an item (leave blank to finish)")
                try:
                    pid_raw = input("Product ID: ").strip()
                except EOFError:
                    print("\nInput ended, finishing item entry.\n")
                    break
                if pid_raw == "":
                    break
                try:
                    pid = int(pid_raw)
                except ValueError:
                    print("Invalid product id.\n"); continue
                prod = find_product_by_id(pid)
                if not prod:
                    print("Product not found.\n"); continue
                try:
                    qty = _prompt_int("Quantity (> 0): ", min_value=1)
                except EOFError:
                    print("\nInput ended, finishing item entry.\n")
                    break
                if prod["stock"] < qty:
                    print("Insufficient stock.\n"); continue
                items.append((pid, qty))
            if not items:
                print("No items added.\n"); continue
            try:
                order_id = create_order(cust["id"], items)
                print(f"Order {order_id} created.\n")
            except ValueError as e:
                print(f"Error: {e}\n")
        elif choice == "6":
            orders = list_orders()
            if not orders:
                print("No orders.\n")
            else:
                for o in orders:
                    print(o)
                    # Show items summary
                    for it in get_order_items(o["order_id"]):
                        print("   ", it)
                print()
        elif choice == "7":
            for r in report_sales_by_product():
                print(r)
            print()
        elif choice == "8":
            if input("Type DELETE to clear ALL data: ").strip() == "DELETE":
                clear_all_data()
                print("All data cleared.\n")
            else:
                print("Cancelled.\n")
        elif choice == "9":
            close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
