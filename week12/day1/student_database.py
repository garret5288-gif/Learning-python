import sqlite3 

conn = sqlite3.connect("students.db") # Connect to SQLite database (or create it)
cur = conn.cursor() # Create a cursor object to interact with the database

cur.execute(''' 
CREATE TABLE IF NOT EXISTS students (
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
)
''')

conn.commit() # Save (commit) the changes

def add_student(name: str, age: int, grade: str) -> None:
    cur.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    conn.commit()

def get_all_students() -> list[dict]:
    # Return students without exposing internal IDs
    cur.execute('SELECT name, age, grade FROM students')
    rows = cur.fetchall()
    return [{"name": row[0], "age": row[1], "grade": row[2]} for row in rows]

def find_student_by_name(name: str) -> list[dict]:
    cur.execute('SELECT name, age, grade FROM students WHERE name = ?', (name,))
    rows = cur.fetchall()
    return [{"name": row[0], "age": row[1], "grade": row[2]} for row in rows]

def delete_student_by_name(name: str) -> None:
    """Delete student(s) by name. If names aren't unique, this removes all matches."""
    cur.execute('DELETE FROM students WHERE name = ?', (name,))
    conn.commit()

def clear_all_students() -> None:
    """Remove all records from the students table."""
    cur.execute('DELETE FROM students')
    conn.commit()

def update_student_by_name(current_name: str, name: str = None, age: int = None, grade: str = None) -> None:
    """Update student fields by current name. If names aren't unique, this updates all matches."""
    fields = []
    values = []
    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if age is not None:
        fields.append("age = ?")
        values.append(age)
    if grade is not None:
        fields.append("grade = ?")
        values.append(grade)
    if not fields:
        return
    values.append(current_name)
    cur.execute(f'UPDATE students SET {", ".join(fields)} WHERE name = ?', values)
    conn.commit()


def close_connection() -> None:
    conn.close()

if __name__ == "__main__":
    # Simple demo so running this file shows it working
    clear_all_students()
    add_student("Alice", 20, "A")
    add_student("Bob", 22, "B")
    print("All:", get_all_students())
    print("Find Alice:", find_student_by_name("Alice"))
    update_student_by_name("Alice", age=21, grade="C")
    print("After update:", get_all_students())
    delete_student_by_name("Bob")
    print("After delete Bob:", get_all_students())
    close_connection()
