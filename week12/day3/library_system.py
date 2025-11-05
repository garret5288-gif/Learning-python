import sqlite3
from datetime import datetime

conn = sqlite3.connect("library.db") # Connect to SQLite database (or create it)
cur = conn.cursor() # Create a cursor object to interact with the database

# Create the books table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0 
)
''')
# Create the borrowers table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS borrowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Create the loans table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    borrower_id INTEGER NOT NULL,
    borrowed_at TEXT NOT NULL DEFAULT (datetime('now')),
    returned_at TEXT,
    FOREIGN KEY(book_id) REFERENCES books(id),
    FOREIGN KEY(borrower_id) REFERENCES borrowers(id)
)
''')

def add_book(title: str, author: str, quantity: int) -> None:
    cur.execute('INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)', (title, author, quantity))
    conn.commit()

def get_all_books() -> list[dict]:
    cur.execute('SELECT id, title, author, quantity FROM books')
    rows = cur.fetchall()
    return [{"id": row[0], "title": row[1], "author": row[2], "quantity": row[3]} for row in rows]

def clear_all_books() -> None:
    """Remove all records from the books table."""
    cur.execute('DELETE FROM books')
    conn.commit()

def close_connection() -> None:
    conn.close()

def add_borrower(name: str, email: str) -> None:
    cur.execute('INSERT INTO borrowers (name, email) VALUES (?, ?)', (name, email))
    conn.commit()

def get_all_borrowers() -> list[dict]:
    cur.execute('SELECT id, name, email FROM borrowers')
    rows = cur.fetchall()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]

def find_borrower_by_email(email: str) -> dict | None:
    cur.execute('SELECT id, name, email FROM borrowers WHERE email = ?', (email,))
    row = cur.fetchone()
    return {"id": row[0], "name": row[1], "email": row[2]} if row else None

def borrow_book(book_title: str, borrower_email: str) -> str:
    """Attempt to borrow a book for a borrower. Returns a status message."""
    # Find book with available quantity
    cur.execute('SELECT id, title, author, quantity FROM books WHERE title = ? LIMIT 1', (book_title,))
    b = cur.fetchone()
    if not b:
        return "Book not found."
    book_id, title, author, qty = b
    if qty <= 0:
        return "No copies available."

    borrower = find_borrower_by_email(borrower_email)
    if not borrower:
        return "Borrower not found."

    # Decrease quantity and insert loan
    cur.execute('UPDATE books SET quantity = quantity - 1 WHERE id = ?', (book_id,))
    cur.execute('INSERT INTO loans (book_id, borrower_id) VALUES (?, ?)', (book_id, borrower["id"]))
    conn.commit()
    return f"{borrower['name']} borrowed '{title}' by {author}."

def return_book(book_title: str, borrower_email: str) -> str:
    """Return one active loan matching the borrower and book. Returns a status message."""
    # Resolve borrower and book ids
    borrower = find_borrower_by_email(borrower_email)
    if not borrower:
        return "Borrower not found."
    cur.execute('SELECT id FROM books WHERE title = ? LIMIT 1', (book_title,))
    row = cur.fetchone()
    if not row:
        return "Book not found."
    book_id = row[0]

    # Find one active loan
    cur.execute('SELECT id FROM loans WHERE borrower_id = ? AND book_id = ? AND returned_at IS NULL LIMIT 1', (borrower["id"], book_id))
    loan = cur.fetchone()
    if not loan:
        return "No active loan found for this borrower and book."

    # Mark returned and increase quantity
    cur.execute("UPDATE loans SET returned_at = datetime('now') WHERE id = ?", (loan[0],))
    cur.execute('UPDATE books SET quantity = quantity + 1 WHERE id = ?', (book_id,))
    conn.commit()
    return "Book returned."

def get_current_loans() -> list[dict]:
    """List all active loans showing who has which book."""
    cur.execute('''
        SELECT l.id, b.title, b.author, br.name, br.email, l.borrowed_at
        FROM loans l
        JOIN books b ON b.id = l.book_id
        JOIN borrowers br ON br.id = l.borrower_id
        WHERE l.returned_at IS NULL
        ORDER BY l.borrowed_at DESC, l.id DESC
    ''')
    rows = cur.fetchall()
    return [{
        "loan_id": r[0],
        "title": r[1],
        "author": r[2],
        "borrower_name": r[3],
        "borrower_email": r[4],
        "borrowed_at": r[5],
    } for r in rows]

def get_loan_history() -> list[dict]:
    """List all loans (past and present)."""
    cur.execute('''
        SELECT l.id, b.title, b.author, br.name, br.email, l.borrowed_at, l.returned_at
        FROM loans l
        JOIN books b ON b.id = l.book_id
        JOIN borrowers br ON br.id = l.borrower_id
        ORDER BY l.borrowed_at DESC, l.id DESC
    ''')
    rows = cur.fetchall()
    return [{
        "loan_id": r[0],
        "title": r[1],
        "author": r[2],
        "borrower_name": r[3],
        "borrower_email": r[4],
        "borrowed_at": r[5],
        "returned_at": r[6],
    } for r in rows]

# ------------- Simple CLI -------------
def _prompt_non_empty(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty.\n")

def _prompt_int(prompt: str, min_value: int = 0) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            iv = int(raw)
            if iv < min_value:
                print(f"Please enter an integer >= {min_value}.\n")
                continue
            return iv
        except ValueError:
            print("Please enter a whole number.\n")

def menu() -> None:
    print("Library System")
    print("1. Add Book")
    print("2. View Books")
    print("3. Add Borrower")
    print("4. View Borrowers")
    print("5. Borrow Book")
    print("6. Return Book")
    print("7. Show Current Loans")
    print("8. Show Loan History")
    print("9. Clear ALL Data")
    print("10. Exit")

def clear_all_data() -> None:
    """Delete all data from loans, borrowers, and books (in that order)."""
    cur.execute('DELETE FROM loans')
    cur.execute('DELETE FROM borrowers')
    cur.execute('DELETE FROM books')
    conn.commit()

def main():
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            title = _prompt_non_empty("Title: ")
            author = _prompt_non_empty("Author: ")
            qty = _prompt_int("Quantity (>= 0): ", 0)
            add_book(title, author, qty)
            print("Book added.\n")
        elif choice == "2":
            for b in get_all_books():
                print(b)
            print()
            if not get_all_books:
                print("No books found.\n")
        elif choice == "3":
            name = _prompt_non_empty("Borrower name: ")
            email = _prompt_non_empty("Borrower email: ")
            try:
                add_borrower(name, email)
                print("Borrower added.\n")
            except sqlite3.IntegrityError:
                print("A borrower with that email already exists.\n")
        elif choice == "4":
            for br in get_all_borrowers():
                print(br)
            print()
        elif choice == "5":
            email = _prompt_non_empty("Borrower email: ")
            title = _prompt_non_empty("Book title to borrow: ")
            msg = borrow_book(title, email)
            print(msg + "\n")
        elif choice == "6":
            email = _prompt_non_empty("Borrower email: ")
            title = _prompt_non_empty("Book title to return: ")
            msg = return_book(title, email)
            print(msg + "\n")
        elif choice == "7":
            loans = get_current_loans()
            if not loans:
                print("No active loans.\n")
            else:
                for l in loans:
                    print(f"{l['borrower_name']} ({l['borrower_email']}) has '{l['title']}' by {l['author']} since {l['borrowed_at']}")
                print()
        elif choice == "8":
            for l in get_loan_history():
                status = f"returned at {l['returned_at']}" if l['returned_at'] else "not yet returned"
                print(f"[{l['loan_id']}] {l['borrower_name']} -> '{l['title']}' ({status}) on {l['borrowed_at']}")
            print()
        elif choice == "9":
            confirm = input("Type DELETE to clear ALL data: ").strip()
            if confirm == "DELETE":
                clear_all_data()
                print("All data cleared.\n")
            else:
                print("Cancelled.\n")
        elif choice == "10":
            close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()


