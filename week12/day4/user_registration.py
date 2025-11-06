import sqlite3

conn = sqlite3.connect("user_registration.db")
cur = conn.cursor()
# Create users table with timestamps if not exists
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    last_login TEXT
)
''')
# Ensure schema has necessary columns
def ensure_schema() -> None:
    """Add columns if missing to support timestamps."""
    cur.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in cur.fetchall()}
    if 'created_at' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT (datetime('now'))")
    if 'last_login' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
    conn.commit()

def is_valid_email(email: str) -> bool:
    # Very simple checks: one '@', dot in domain, no spaces
    if not email or ' ' in email:
        return False
    if email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if not local or not domain or '.' not in domain:
        return False
    if domain.startswith('.') or domain.endswith('.'):
        return False
    return True

def is_strong_password(pw: str) -> bool:
    # Length >= 8, at least one letter and one digit
    if len(pw) < 8:
        return False
    has_alpha = False
    has_digit = False
    for ch in pw:
        if ch.isalpha():
            has_alpha = True
        if ch.isdigit():
            has_digit = True
        if has_alpha and has_digit:
            return True
    return False

def register_user(username: str, email: str, password: str) -> None:
    # Normalize
    username = username.strip().lower()
    email = email.strip().lower()
    if not is_valid_email(email):
        print("Invalid email format.")
        return
    if not is_strong_password(password):
        print("Weak password: use 8+ characters with letters and digits.")
        return
    try:
        cur.execute('''
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("User with this username or email already exists.")

def close_connection() -> None:
    conn.close()

def login_user(username: str, password: str) -> bool:
    # Normalize
    username = username.strip().lower()
    cur.execute('''
    SELECT id FROM users WHERE LOWER(username) = ? AND password = ?
    ''', (username, password))
    row = cur.fetchone()
    if not row:
        return False
    user_id = row[0]
    # Update last_login timestamp
    cur.execute("UPDATE users SET last_login = datetime('now') WHERE id = ?", (user_id,))
    conn.commit()
    return True
# Retrieve all users
def get_all_users() -> list[dict]:
    cur.execute('''
    SELECT username, email, created_at, last_login FROM users ORDER BY id
    ''')
    rows = cur.fetchall()
    return [
        {
            'username': r[0],
            'email': r[1],
            'created_at': r[2],
            'last_login': r[3],
        } for r in rows
    ]

def menu(current_user: str | None = None):
    print("User Registration System")
    print("1. Register User")
    print("2. Login User")
    print("3. Logout User")
    print("4. View all users")
    print("5. Exit")
    if current_user:
        print(f"(Logged in as: {current_user})")

def prompt_non_empty(prompt: str) -> str:
    """Prompt until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.\n")

def logout_user() -> None:
    print("User logged out successfully.\n")

def main():
    ensure_schema()
    current_user = None
    while True:
        menu(current_user)
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            username = prompt_non_empty("Enter username: ")
            email = prompt_non_empty("Enter email: ")
            password = prompt_non_empty("Enter password: ")
            confirm = prompt_non_empty("Confirm password: ")
            if password != confirm:
                print("Passwords do not match.\n")
            else:
                register_user(username, email, password)
                print("User registered successfully!\n")
        elif choice == '2':
            if current_user:
                print("Already logged in. Please logout first.\n")
            else:
                username = prompt_non_empty("Enter username: ")
                password = prompt_non_empty("Enter password: ")
                if login_user(username, password):
                    current_user = username.strip().lower()
                    print("Login successful!\n")
                else:
                    print("Invalid username or password.\n")
        elif choice == '3':
            if current_user:
                logout_user()
                current_user = None
            else:
                print("No user is currently logged in.\n")
        elif choice == '4':
            users = get_all_users()
            if not users:
                print("No users found.\n")
            else:
                for idx, u in enumerate(users, 1):
                    created = u['created_at'] or 'N/A'
                    last = u['last_login'] or 'never'
                    print(f"{idx}. {u['username']} | {u['email']} | created: {created} | last login: {last}")
                print()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")
    close_connection()

if __name__ == "__main__":
    main()