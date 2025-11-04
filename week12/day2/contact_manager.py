import sqlite3

conn = sqlite3.connect("contacts.db") # Connect to SQLite database (or create it)
cur = conn.cursor() # Create a cursor object to interact with the database

cur.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
''')

def add_contact(name: str, phone: str, email: str) -> None:
    cur.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()

def get_all_contacts() -> list[dict]:
    cur.execute('SELECT name, phone, email FROM contacts')
    rows = cur.fetchall()
    return [{"name": row[0], "phone": row[1], "email": row[2]} for row in rows]

def find_contact_by_name(name: str) -> list[dict]:
    cur.execute('SELECT name, phone, email FROM contacts WHERE name = ?', (name,))
    rows = cur.fetchall()
    return [{"name": row[0], "phone": row[1], "email": row[2]} for row in rows]

def update_contact(name: str, phone: str = None, email: str = None) -> None:
    fields = []
    values = []
    if phone is not None:
        fields.append("phone = ?")
        values.append(phone)
    if email is not None:
        fields.append("email = ?")
        values.append(email)
    if not fields:
        return
    values.append(name)
    cur.execute(f'UPDATE contacts SET {", ".join(fields)} WHERE name = ?', values)
    conn.commit()

def delete_contact(name: str) -> None:
    cur.execute('DELETE FROM contacts WHERE name = ?', (name,))
    conn.commit()

def close_connection() -> None:
    conn.close()

# -------- Input helpers --------
def prompt_non_empty(prompt: str) -> str:
    """Prompt until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.\n")

def menu() -> None:
    print("Contact Manager")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Find Contact by Name")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def main():
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = prompt_non_empty("Name: ")
            phone = prompt_non_empty("Phone: ")
            email = prompt_non_empty("Email: ")
            add_contact(name, phone, email)
            print("Contact added.\n")
        elif choice == "2":
            contacts = get_all_contacts()
            for c in contacts:
                print(c)
            print()
        elif choice == "3":
            name = prompt_non_empty("Name to find: ")
            contacts = find_contact_by_name(name)
            for c in contacts:
                print(c)
            print()
        elif choice == "4":
            name = prompt_non_empty("Name of contact to update: ")
            phone = input("New Phone (or blank to keep current): ").strip()
            email = input("New Email (or blank to keep current): ").strip()
            update_contact(
                name,
                phone=phone if phone else None,
                email=email if email else None
            )
            print("Contact updated.\n")
        elif choice == "5":
            name = prompt_non_empty("Name of contact to delete: ")
            delete_contact(name)
            print("Contact deleted.\n")
        elif choice == "6":
            close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()