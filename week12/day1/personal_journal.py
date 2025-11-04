import sqlite3
import datetime

conn = sqlite3.connect("journal.db")  # Connect to SQLite database (or create it)
cur = conn.cursor()  # Create a cursor object to interact with the database

cur.execute('''
CREATE TABLE IF NOT EXISTS entries (
    date TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

# Index to speed up lookups by date
cur.execute('CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date)')

def add_entry(entry_date: str, content: str) -> None:
    cur.execute('INSERT INTO entries (date, content) VALUES (?, ?)', (entry_date, content))
    conn.commit()

def add_today_entry(content: str) -> None:
    """Convenience: add an entry with today's date and a time-stamped header."""
    today = datetime.date.today().isoformat()
    stamp = datetime.datetime.now().strftime("%H:%M")
    text = f"[{stamp}]\n{content}"
    add_entry(today, text)

def get_all_entries():
    # Stable order: newest dates first, then newest inserted first for same day
    cur.execute('SELECT date, content FROM entries ORDER BY date DESC, rowid DESC')
    rows = cur.fetchall()
    return [{"date": row[0], "content": row[1]} for row in rows]

def find_entries_by_date(entry_date: str):
    cur.execute('SELECT date, content FROM entries WHERE date = ?', (entry_date,))
    rows = cur.fetchall()
    return [{"date": row[0], "content": row[1]} for row in rows]

def delete_entries_by_date(entry_date: str) -> None:
    """Delete entry(ies) by date. If dates aren't unique, this removes all matches."""
    cur.execute('DELETE FROM entries WHERE date = ?', (entry_date,))
    conn.commit()

def clear_all_entries() -> None:
    """Remove all records from the entries table."""
    cur.execute('DELETE FROM entries')
    conn.commit()

def update_entries_by_date(current_date: str, new_date: str = None, new_content: str = None) -> None:
    """Update entry fields by current date. If dates aren't unique, this updates all matches."""
    fields = []
    values = []
    if new_date is not None:
        fields.append("date = ?")
        values.append(new_date)
    if new_content is not None:
        fields.append("content = ?")
        values.append(new_content)
    if not fields:
        return
    values.append(current_date)
    cur.execute(f'UPDATE entries SET {", ".join(fields)} WHERE date = ?', values)
    conn.commit()

def close_connection() -> None:
    conn.close()

if __name__ == "__main__":
    # Simple demo so running this file shows it working
    clear_all_entries()
    add_today_entry("Started my personal journal.")
    add_today_entry("Wrote another entry for today.")
    add_entry("2024-06-01", "This is an entry from June 1st.")
    print("All entries:", get_all_entries())
    print("Entries for today:", find_entries_by_date(datetime.date.today().isoformat()))
    update_entries_by_date("2024-06-01", new_content="Updated June 1st entry.")
    print("After update:", get_all_entries())
    delete_entries_by_date(datetime.date.today().isoformat())
    print("After deleting today's entries:", get_all_entries())
    close_connection()

