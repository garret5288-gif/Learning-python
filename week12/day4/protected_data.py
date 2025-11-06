import sqlite3

conn = sqlite3.connect('fish_data.db')
cur = conn.cursor()
# Create users table with timestamps if not exists
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fish_type TEXT NOT NULL,
    weight REAL NOT NULL,
    length REAL NOT NULL,
    caught_at TEXT DEFAULT (datetime('now')),
    location TEXT,
    notes TEXT
)
''')

# Authentication/Authorization schema (simple)
cur.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','viewer'))
)
''')

# Table to store the current session user for audit triggers
cur.execute('''
CREATE TABLE IF NOT EXISTS session_info (
    current_user TEXT
)
''')
# Ensure schema has necessary columns
def ensure_schema():
    """Add columns if missing to support timestamps."""
    cur.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in cur.fetchall()}
    if 'caught_at' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN caught_at TEXT DEFAULT (datetime('now'))")
    if 'location' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN location TEXT")
    if 'notes' not in cols:
        cur.execute("ALTER TABLE users ADD COLUMN notes TEXT")
    conn.commit()

def add_fish(fish_type: str, weight: float, length: float, location: str = "", notes: str = "") -> None:
    cur.execute('''
    INSERT INTO users (fish_type, weight, length, location, notes)
    VALUES (?, ?, ?, ?, ?)
    ''', (fish_type, weight, length, location, notes))
    conn.commit()

def get_all_fish() -> list[dict]:
    cur.execute('''
    SELECT id, fish_type, weight, length, caught_at, location, notes FROM users ORDER BY id
    ''')
    rows = cur.fetchall()
    fish_list = []
    for row in rows:
        fish_list.append({
            "id": row[0],
            "fish_type": row[1],
            "weight": row[2],
            "length": row[3],
            "caught_at": row[4],
            "location": row[5],
            "notes": row[6]
        })
    return fish_list

def delete_fish(fish_id: int):
    # Return True if a row was deleted, False otherwise
    cur.execute("DELETE FROM users WHERE id = ?", (fish_id,))
    conn.commit()
    return cur.rowcount > 0

def auth_menu():
    print("\n=== Fish Catch Logger ===\n")
    print("1. Login")
    print("2. Create Account (viewer)")
    print("3. Exit\n")

def menu_authed(current_user: str, role: str):
    print("\n=== Fish Catch Logger ===\n")
    print(f"User: {current_user} | Role: {role}\n")
    print("1. Add Fish Catch")
    print("2. View All Fish Catches")
    print("3. Delete Fish Catch (admin only)")
    print("4. View Audit Log (admin only)")
    print("5. Logout")
    print("6. Exit\n")

def ensure_audit_schema() -> None:
        """Create audit log and triggers for INSERT/UPDATE/DELETE."""
        cur.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                action TEXT NOT NULL,
                row_id INTEGER,
                changed_by TEXT,
                changed_at TEXT DEFAULT (datetime('now')),
                details TEXT
        )
        ''')
        def has_trigger(name: str) -> bool:
                cur.execute("SELECT 1 FROM sqlite_master WHERE type='trigger' AND name=?", (name,))
                return cur.fetchone() is not None
        # Triggers for fish catches table (users)
        if not has_trigger('trg_users_ai'):
                cur.execute('''
                CREATE TRIGGER trg_users_ai AFTER INSERT ON users
                BEGIN
                    INSERT INTO audit_log(table_name, action, row_id, changed_by, details)
                    VALUES(
                        'users','INSERT', NEW.id,
                        (SELECT current_user FROM session_info LIMIT 1),
                        'fish_type='||quote(NEW.fish_type)||', weight='||NEW.weight||', length='||NEW.length||', location='||quote(NEW.location)||', notes='||quote(NEW.notes)
                    );
                END;
                ''')
# Triggers for UPDATE            
        if not has_trigger('trg_users_au'):
                cur.execute('''
                CREATE TRIGGER trg_users_au AFTER UPDATE ON users
                BEGIN
                    INSERT INTO audit_log(table_name, action, row_id, changed_by, details)
                    VALUES(
                        'users','UPDATE', NEW.id,
                        (SELECT current_user FROM session_info LIMIT 1),
                        'updated'
                    );
                END;
                ''')
# Triggers for DELETE need to capture OLD values              
        if not has_trigger('trg_users_ad'):
                cur.execute('''
                CREATE TRIGGER trg_users_ad AFTER DELETE ON users
                BEGIN
                    INSERT INTO audit_log(table_name, action, row_id, changed_by, details)
                    VALUES(
                        'users','DELETE', OLD.id,
                        (SELECT current_user FROM session_info LIMIT 1),
                        'fish_type='||quote(OLD.fish_type)||', weight='||OLD.weight||', length='||OLD.length||', location='||quote(OLD.location)||', notes='||quote(OLD.notes)
                    );
                END;
                ''')
        # Triggers for accounts table
        if not has_trigger('trg_accounts_ai'):
                cur.execute('''
                CREATE TRIGGER trg_accounts_ai AFTER INSERT ON accounts
                BEGIN
                    INSERT INTO audit_log(table_name, action, row_id, changed_by, details)
                    VALUES(
                        'accounts','INSERT', NEW.id,
                        (SELECT current_user FROM session_info LIMIT 1),
                        'username='||quote(NEW.username)||', role='||quote(NEW.role)
                    );
                END;
                ''')
        # Triggers for UPDATE
        if not has_trigger('trg_accounts_au'):
                cur.execute('''
                CREATE TRIGGER trg_accounts_au AFTER UPDATE ON accounts
                BEGIN
                    INSERT INTO audit_log(table_name, action, row_id, changed_by, details)
                    VALUES(
                        'accounts','UPDATE', NEW.id,
                        (SELECT current_user FROM session_info LIMIT 1),
                        'username='||quote(NEW.username)||', role='||quote(NEW.role)
                    );
                END;
                ''')
        # Triggers for DELETE need to capture OLD values
        if not has_trigger('trg_accounts_ad'):
                cur.execute('''
                CREATE TRIGGER trg_accounts_ad AFTER DELETE ON accounts
                BEGIN
                    INSERT INTO audit_log(table_name, action, row_id, changed_by, details)
                    VALUES(
                        'accounts','DELETE', OLD.id,
                        (SELECT current_user FROM session_info LIMIT 1),
                        'username='||quote(OLD.username)||', role='||quote(OLD.role)
                    );
                END;
                ''')
        conn.commit()

def get_audit_log(limit: int = 50) -> list[dict]: # Retrieve recent audit log entries
        cur.execute('''
        SELECT id, changed_at, changed_by, table_name, action, row_id, details
        FROM audit_log
        ORDER BY id DESC
        LIMIT ?
        ''', (limit,))
        rows = cur.fetchall()
        return [
                {
                        'id': r[0], 'changed_at': r[1], 'changed_by': r[2],
                        'table_name': r[3], 'action': r[4], 'row_id': r[5], 'details': r[6]
                } for r in rows
        ]

def set_current_user(username: str | None) -> None: # Set current session user for audit logging
        cur.execute('DELETE FROM session_info')
        if username:
                cur.execute('INSERT INTO session_info(current_user) VALUES (?)', (username,))
        conn.commit()

def ensure_initial_admin() -> None: # Ensure the initial admin user exists
    """If there are no accounts, prompt to create the first admin user."""
    cur.execute("SELECT COUNT(1) FROM accounts")
    count = cur.fetchone()[0]
    if count == 0:
        print("No users found. Let's create the first admin account.\n")
        while True:
            username = prompt_non_empty("Admin username: ")
            password = prompt_non_empty("Admin password: ")
            confirm = prompt_non_empty("Confirm password: ")
            if password != confirm:
                print("Passwords do not match. Try again.\n")
                continue
            try:
                cur.execute(
                    "INSERT INTO accounts (username, password, role) VALUES (?, ?, 'admin')",
                    (username.strip(), password.strip()),
                )
                conn.commit()
                print("Admin account created.\n")
                break
            except sqlite3.IntegrityError:
                print("Username already exists. Choose another.\n")

def authenticate(username: str, password: str) -> tuple[str, str] | None: # Authenticate user and return (username, role) or None
    cur.execute("SELECT username, role FROM accounts WHERE username = ? AND password = ?",
                (username.strip(), password.strip()))
    row = cur.fetchone()
    if not row:
        return None
    return row[0], row[1]

def create_user(username: str, password: str, role: str) -> bool:
    """Create a new account. Returns True on success, False otherwise."""
    role_norm = role.strip().lower()
    if role_norm not in ("admin", "viewer"):
        print("Invalid role. Use 'admin' or 'viewer'.")
        return False
    try:
        cur.execute(
            "INSERT INTO accounts (username, password, role) VALUES (?, ?, ?)",
            (username.strip(), password.strip(), role_norm)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Username already exists.")
        return False

def prompt_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Value cannot be empty.\n")

def prompt_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.\n")

def prompt_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.\n")

def main():
    ensure_schema()          # ensure catches schema is up to date
    ensure_audit_schema()    # ensure audit log and triggers
    ensure_initial_admin()   # interactive first-run setup
    try:
        while True:
            # Pre-login menu
            auth_menu()
            pre_choice = input("Choose an option: ").strip()
            if pre_choice == "1":
                username = prompt_non_empty("Username: ")
                password = prompt_non_empty("Password: ")
                auth = authenticate(username, password)
                if not auth:
                    print("Invalid credentials. Try again.\n")
                    continue
                current_user, role = auth
                set_current_user(current_user)

                # Authorized session loop
                while True:
                    menu_authed(current_user, role)
                    choice = input("Choose an option: ").strip()
                    if choice == "1":
                        fish_type = prompt_non_empty("Enter fish type: ")
                        weight = prompt_float("Enter weight (lbs): ")
                        length = prompt_float("Enter length (inches): ")
                        location = input("Enter location (optional): ").strip()
                        notes = input("Enter notes (optional): ").strip()
                        add_fish(fish_type, weight, length, location, notes)
                        print("Fish catch added.\n")
                    elif choice == "2":
                        fish_list = get_all_fish()
                        if not fish_list:
                            print("No fish catches found.\n")
                        else:
                            for i, fish in enumerate(fish_list, 1):
                                print(f"{i}. ID {fish['id']} | Type: {fish['fish_type']}, Weight: {fish['weight']} lbs, Length: {fish['length']} inches, Caught At: {fish['caught_at']}, Location: {fish['location']}, Notes: {fish['notes']}")
                            print()
                    elif choice == "3":
                        if role != "admin":
                            print("Not authorized. Admins only.\n")
                            continue
                        fish_id = prompt_int("Enter fish ID to delete: ")
                        if delete_fish(fish_id):
                            print("Fish catch deleted.\n")
                        else:
                            print("No such ID. Nothing deleted.\n")
                    elif choice == "4":
                        if role != "admin":
                            print("Not authorized. Admins only.\n")
                            continue
                        logs = get_audit_log(100)
                        if not logs:
                            print("No audit entries found.\n")
                        else:
                            for entry in logs:
                                who = entry['changed_by'] if entry['changed_by'] else 'unknown'
                                print(f"#{entry['id']} [{entry['changed_at']}] by {who} -> {entry['table_name']} {entry['action']} row {entry['row_id']} | {entry['details']}")
                            print()
                    elif choice == "5":
                        print("Logged out.\n")
                        set_current_user(None)
                        break
                    elif choice == "6":
                        print("Exiting...")
                        set_current_user(None)
                        return
                    else:
                        print("Invalid choice. Please try again.\n")
            elif pre_choice == "2":
                # Self-signup for viewer accounts
                print("\nCreate a new viewer account\n")
                while True:
                    new_user = prompt_non_empty("Choose a username: ")
                    new_pass = prompt_non_empty("Choose a password: ")
                    confirm = prompt_non_empty("Confirm password: ")
                    if new_pass != confirm:
                        print("Passwords do not match. Try again.\n")
                        continue
                    try:
                        cur.execute(
                            "INSERT INTO accounts (username, password, role) VALUES (?, ?, 'viewer')",
                            (new_user.strip(), new_pass.strip())
                        )
                        conn.commit()
                        print("Account created. You can now log in.\n")
                        break
                    except sqlite3.IntegrityError:
                        print("Username already exists. Choose another.\n")
                continue
            elif pre_choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.\n")
    finally:
        try:
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()