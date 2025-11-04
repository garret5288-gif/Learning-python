import sqlite3
from datetime import datetime 

conn = sqlite3.connect("expenses.db") # Connect to SQLite database (or create it)
cur = conn.cursor() # Create a cursor object to interact with the database
# Create the expenses table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT
)
''')

def add_expense(date: str, amount: float, category: str, description: str = None) -> None:
    cur.execute('INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)', 
                (date, amount, category, description))
    conn.commit()

def get_all_expenses() -> list[dict]:
    cur.execute('SELECT date, amount, category, description FROM expenses')
    rows = cur.fetchall()
    return [{"date": row[0], "amount": row[1], "category": row[2], "description": row[3]} for row in rows]

def find_expenses_by_category(category: str) -> list[dict]:
    cur.execute('SELECT date, amount, category, description FROM expenses WHERE category = ?', (category,))
    rows = cur.fetchall()
    return [{"date": row[0], "amount": row[1], "category": row[2], "description": row[3]} for row in rows]

def delete_expenses_by_category(category: str) -> None:
    """Delete expense(s) by category. If categories aren't unique, this removes all matches."""
    cur.execute('DELETE FROM expenses WHERE category = ?', (category,))
    conn.commit()

def clear_all_expenses() -> None:
    """Remove all records from the expenses table."""
    cur.execute('DELETE FROM expenses')
    conn.commit()

def update_expenses_by_category(current_category: str, date: str = None, amount: float = None, category: str = None, description: str = None) -> None:
    """Update expense fields by current category. If categories aren't unique, this updates all matches."""
    fields = []
    values = []
    if date is not None:
        fields.append("date = ?")
        values.append(date)
    if amount is not None:
        fields.append("amount = ?")
        values.append(amount)
    if category is not None:
        fields.append("category = ?")
        values.append(category)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if not fields:
        return
    values.append(current_category)
    cur.execute(f'UPDATE expenses SET {", ".join(fields)} WHERE category = ?', values)
    conn.commit()

def close_connection() -> None:
    """Close the database connection."""
    conn.close()

# -------- Input helpers --------
def prompt_non_empty(prompt: str) -> str:
    """Prompt until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.\n")

def prompt_amount(prompt: str) -> float:
    """Prompt for a positive number amount; re-prompt on invalid input."""
    while True:
        raw = input(prompt).strip()
        try:
            amt = float(raw)
            if amt <= 0:
                print("Amount must be greater than 0.\n")
                continue
            return amt
        except ValueError:
            print("Please enter a valid number (e.g., 12.34).\n")

def prompt_amount_optional(prompt: str):
    """Prompt for amount; returns float or None if blank; re-prompt on invalid number."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            amt = float(raw)
            if amt <= 0:
                print("Amount must be greater than 0, or leave blank to keep current.\n")
                continue
            return amt
        except ValueError:
            print("Please enter a valid number (e.g., 12.34) or leave blank.\n")

def prompt_date_or_today(prompt: str) -> str:
    """Prompt for date; if blank, default to today; validate format YYYY-MM-DD."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            # Validate date format
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Please enter a date in YYYY-MM-DD format, or leave blank for today.\n")

def prompt_date_optional(prompt: str):
    """Prompt for date; returns YYYY-MM-DD or None if blank; validates format."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Please enter a date in YYYY-MM-DD format, or leave blank to keep current.\n")

def menu():
    print("Expense Tracker Menu:")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Find Expenses by Category")
    print("4. Update Expenses by Category")
    print("5. Delete Expenses by Category")
    print("6. Clear All Expenses")
    print("7. Exit")

def main():
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            date = prompt_date_or_today("Date (YYYY-MM-DD) [default today]: ")
            amount = prompt_amount("Amount: ")
            category = prompt_non_empty("Category: ")
            description = input("Description (optional): ").strip() or None
            add_expense(date, amount, category, description)
            print("Expense added.\n")
        elif choice == "2":
            expenses = get_all_expenses()
            for e in expenses:
                print(e)
            print()
            if not expenses:
                print("No expenses found.\n")
        elif choice == "3":
            category = prompt_non_empty("Category to find: ")
            expenses = find_expenses_by_category(category)
            for e in expenses:
                print(e)
            print()
        elif choice == "4":
            current_category = prompt_non_empty("Current Category to update: ")
            date = prompt_date_optional("New Date (YYYY-MM-DD) (or blank to keep current): ")
            amount = prompt_amount_optional("New Amount (or blank to keep current): ")
            category = input("New Category (or blank to keep current): ").strip() or None
            description = input("New Description (or blank to keep current): ").strip() or None
            update_expenses_by_category(current_category, date, amount, category, description)
            print("Expenses updated.\n")
        elif choice == "5":
            category = prompt_non_empty("Category of expenses to delete: ")
            delete_expenses_by_category(category)
            print("Expenses deleted.\n")
        elif choice == "6":
            clear_all_expenses()
            print("All expenses cleared.\n")
        elif choice == "7":
            close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()