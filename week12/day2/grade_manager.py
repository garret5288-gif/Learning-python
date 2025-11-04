import sqlite3

conn = sqlite3.connect("student_grades.db") # Connect to SQLite database (or create it)

cur = conn.cursor() # Create a cursor object to interact with the database

cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    first_name TEXT NOT NULL,
    math_grade REAL,
    science_grade REAL,
    english_grade REAL
)
''')

def add_student(first_name: str, math_grade: float = None, science_grade: float = None, english_grade: float = None) -> None:
    cur.execute('INSERT INTO students (first_name, math_grade, science_grade, english_grade) VALUES (?, ?, ?, ?)', 
                (first_name, math_grade, science_grade, english_grade))
    conn.commit()

def get_all_students() -> list[dict]:
    cur.execute('SELECT first_name, math_grade, science_grade, english_grade FROM students')
    rows = cur.fetchall()
    return [{"first_name": row[0], "math_grade": row[1], "science_grade": row[2], "english_grade": row[3]} for row in rows]

def find_student_by_name(first_name: str) -> list[dict]:
    cur.execute('SELECT first_name, math_grade, science_grade, english_grade FROM students WHERE first_name = ?', (first_name,))
    rows = cur.fetchall()
    return [{"first_name": row[0], "math_grade": row[1], "science_grade": row[2], "english_grade": row[3]} for row in rows]

def delete_student_by_name(first_name: str) -> None:
    """Delete student(s) by first name. If names aren't unique, this removes all matches."""
    cur.execute('DELETE FROM students WHERE first_name = ?', (first_name,))
    conn.commit()

def clear_all_students() -> None:
    """Remove all records from the students table."""
    cur.execute('DELETE FROM students')
    conn.commit()

def update_student_by_name(current_name: str, first_name: str = None, math_grade: float = None, science_grade: float = None, english_grade: float = None) -> None:
    """Update student fields by current first name. If names aren't unique, this updates all matches."""
    fields = []
    values = []
    if first_name is not None:
        fields.append("first_name = ?")
        values.append(first_name)
    if math_grade is not None:
        fields.append("math_grade = ?")
        values.append(math_grade)
    if science_grade is not None:
        fields.append("science_grade = ?")
        values.append(science_grade)
    if english_grade is not None:
        fields.append("english_grade = ?")
        values.append(english_grade)
    if not fields:
        return
    values.append(current_name)
    cur.execute(f'UPDATE students SET {", ".join(fields)} WHERE first_name = ?', values)
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

def prompt_grade(prompt: str):
    """Prompt for a grade: returns float or None if left blank. Re-prompts on invalid input."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number (e.g., 92.5) or leave blank.\n")

def menu() -> None:
    print("Student Grade Manager")
    print("---------------------")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Find Student by Name")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Clear All Students")
    print("7. Exit")

def main():
    while True:
        menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            fn = prompt_non_empty("First name: ")
            mg = prompt_grade("Math grade (or blank): ")
            sg = prompt_grade("Science grade (or blank): ")
            eg = prompt_grade("English grade (or blank): ")
            add_student(fn, mg, sg, eg)
            print("Student added.\n")
        elif choice == "2":
            students = get_all_students()
            for s in students:
                print(s)
            print()
            if not students:
                print("No students found.\n")
        elif choice == "3":
            fn = prompt_non_empty("First name to find: ")
            students = find_student_by_name(fn)
            for s in students:
                print(s)
            print()
        elif choice == "4":
            current_name = prompt_non_empty("Current first name of student to update: ")
            new_name = input("New first name (or blank to keep current): ").strip()
            mg = prompt_grade("New Math grade (or blank to keep current): ")
            sg = prompt_grade("New Science grade (or blank to keep current): ")
            eg = prompt_grade("New English grade (or blank to keep current): ")
            update_student_by_name(
                current_name,
                first_name=new_name if new_name else None,
                math_grade=mg,
                science_grade=sg,
                english_grade=eg
            )
            print("Student updated.\n")
        elif choice == "5":
            fn = prompt_non_empty("First name of student to delete: ")
            delete_student_by_name(fn)
            print("Student(s) deleted.\n")
        elif choice == "6":
            clear_all_students()
            print("All students cleared.\n")
        elif choice == "7":
            close_connection()
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.\n")

if __name__ == "__main__":
    main()