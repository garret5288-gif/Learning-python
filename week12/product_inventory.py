import sqlite3

conn = sqlite3.connect('products.db')
cur = conn.cursor()
# Create products table
cur.execute('''
CREATE TABLE IF NOT EXISTS products (
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')

def add_product(name: str, quantity: int, price: float) -> None:
    cur.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()

def get_all_products() -> list[dict]:
    cur.execute('SELECT name, quantity, price FROM products')
    rows = cur.fetchall()
    return [{"name": row[0], "quantity": row[1], "price": row[2]} for row in rows]

def find_product_by_name(name: str) -> list[dict]:
    cur.execute('SELECT name, quantity, price FROM products WHERE name = ?', (name,))
    rows = cur.fetchall()
    return [{"name": row[0], "quantity": row[1], "price": row[2]} for row in rows]

def delete_product_by_name(name: str) -> None:
    cur.execute('DELETE FROM products WHERE name = ?', (name,))
    conn.commit()

def clear_all_products() -> None:
    cur.execute('DELETE FROM products')
    conn.commit()

def update_product_by_name(current_name: str, name: str = None, quantity: int = None, price: float = None) -> None:
    fields = []
    values = []
    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if quantity is not None:
        fields.append("quantity = ?")
        values.append(quantity)
    if price is not None:
        fields.append("price = ?")
        values.append(price)
    if not fields:
        return
    values.append(current_name)
    cur.execute(f'UPDATE products SET {", ".join(fields)} WHERE name = ?', values)
    conn.commit()

def show_table(): # Display all products in the table
    cur.execute('SELECT * FROM products')
    rows = cur.fetchall()
    for row in rows:
        print(row)

def close_connection() -> None:
    conn.close()

if __name__ == "__main__":
    # Simple demo so running this file shows it working
    clear_all_products()
    add_product("Laptop", 10, 999.99)
    add_product("Mouse", 50, 19.99)
    add_product("Keyboard", 30, 49.99)
    add_product("Monitor", 20, 199.99)
    add_product("Printer", 15, 149.99)
    print("All Products:", get_all_products())
    print("Find Laptop:", find_product_by_name("Laptop"))
    update_product_by_name("Laptop", quantity=5, price=899.99)
    print("After update:", get_all_products())
    delete_product_by_name("Mouse")
    print("After delete Mouse:", get_all_products())
    show_table()
    close_connection()
