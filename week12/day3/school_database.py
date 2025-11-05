import sqlite3

conn = sqlite3.connect("school.db")  # Connect to SQLite database (or create it)
cur = conn.cursor()  # Create a cursor object to interact with the database

# Ensure foreign key constraints are enforced
cur.execute("PRAGMA foreign_keys = ON;")

# Create the students table if it doesn't exist
cur.execute(
    '''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade_level TEXT NOT NULL
)
'''
)

cur.execute(
    '''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    instructor TEXT NOT NULL
)
'''
)

cur.execute(
    '''
CREATE TABLE IF NOT EXISTS enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
'''
)

def add_student(name: str, age: int, grade_level: str) -> None:
    cur.execute(
        'INSERT INTO students (name, age, grade_level) VALUES (?, ?, ?)',
        (name, age, grade_level),
    )
    conn.commit()

def get_all_students() -> list[dict]:
    cur.execute('SELECT id, name, age, grade_level FROM students ORDER BY id')
    rows = cur.fetchall()
    return [
        {"id": row[0], "name": row[1], "age": row[2], "grade_level": row[3]}
        for row in rows
    ]

def find_student_by_name(name: str) -> list[dict]:
    # Case-insensitive match
    cur.execute('SELECT id, name, age, grade_level FROM students WHERE name = ? COLLATE NOCASE', (name,))
    rows = cur.fetchall()
    return [
        {"id": row[0], "name": row[1], "age": row[2], "grade_level": row[3]}
        for row in rows
    ]

def delete_student_by_name(name: str) -> None:
    """Delete student(s) by name. If names aren't unique, this removes all matches."""
    cur.execute('DELETE FROM students WHERE name = ?', (name,))
    conn.commit()

def clear_all_students() -> None:
    """Remove all records from the students table."""
    cur.execute('DELETE FROM students')
    conn.commit()

def close_connection() -> None:
    try:
        conn.close()
    except Exception:
        pass

def add_course(course_name: str, instructor: str) -> None:
    cur.execute(
        'INSERT INTO courses (course_name, instructor) VALUES (?, ?)',
        (course_name, instructor),
    )
    conn.commit()

def get_all_courses() -> list[dict]:
    cur.execute('SELECT id, course_name, instructor FROM courses ORDER BY id')
    rows = cur.fetchall()
    return [
        {"id": row[0], "course_name": row[1], "instructor": row[2]}
        for row in rows
    ]

def find_course_by_name(course_name: str) -> list[dict]:
    # Case-insensitive match; return potentially multiple if duplicates exist
    cur.execute('SELECT id, course_name, instructor FROM courses WHERE course_name = ? COLLATE NOCASE', (course_name,))
    rows = cur.fetchall()
    return [
        {"id": row[0], "course_name": row[1], "instructor": row[2]}
        for row in rows
    ]


PRESET_COURSES: list[tuple[str, str]] = [
    ("Math 101", "Dr. Smith"),
    ("History 201", "Ms. Lee"),
    ("Biology 150", "Dr. Patel"),
    ("English 102", "Mr. Johnson"),
    ("Computer Science 101", "Prof. Kim"),
]


def seed_courses() -> None:
    for name, instructor in PRESET_COURSES:
        cur.execute('SELECT id FROM courses WHERE course_name = ?', (name,))
        if not cur.fetchone():
            add_course(name, instructor)

def enroll_student(student_id: int, course_id: int) -> None:
    # Store a placeholder for enrollment_date since dates are not used
    cur.execute(
        'INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (?, ?, ?)',
        (student_id, course_id, 'N/A'),
    )
    conn.commit()

def get_enrollments() -> list[dict]:
    cur.execute('SELECT student_id, course_id FROM enrollments')
    rows = cur.fetchall()
    return [
        {
            "student_id": row[0],
            "course_id": row[1],
        }
        for row in rows
    ]


def get_course_roster(course_id: int) -> list[dict]:
    cur.execute(
        '''
        SELECT s.id, s.name, s.grade_level
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        WHERE e.course_id = ?
        ORDER BY s.id
        ''',
        (course_id,),
    )
    rows = cur.fetchall()
    return [
        {
            "student_id": row[0],
            "name": row[1],
            "grade_level": row[2],
        }
        for row in rows
    ]

def clear_all_data() -> None:
    # Delete in FK-safe order (preserve courses)
    cur.execute('DELETE FROM enrollments')
    cur.execute('DELETE FROM students')
    conn.commit()


# ---------------- CLI helpers -----------------
def _prompt_non_empty(prompt: str) -> str:
    while True:
        try:
            val = input(prompt).strip()
        except EOFError:
            raise
        if val:
            return val
        print("Value cannot be empty.")


def _prompt_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        try:
            raw = input(prompt).strip()
        except EOFError:
            raise
        try:
            val = int(raw)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if min_val is not None and val < min_val:
            print(f"Value must be >= {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"Value must be <= {max_val}.")
            continue
        return val


# No date handling needed


def main() -> None:
    # Ensure courses exist
    seed_courses()
    while True:
        print("\nSchool Database Menu")
        print("1. Add student")
        print("2. View students")
        print("3. View courses")
        print("4. Enroll student in course")
        print("5. View all course rosters")
        print("6. Clear student/enrollment data")
        print("7. Exit")
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            print("\nGoodbye!")
            close_connection()
            return

        if choice == "1":
            try:
                name = _prompt_non_empty("Name: ")
                age = _prompt_int("Age: ", min_val=1)
                grade_level = _prompt_non_empty("Grade level (e.g., 9th, 10th): ")
                add_student(name, age, grade_level)
                print("Student added.")
            except EOFError:
                print("Input ended.")

        elif choice == "2":
            students = get_all_students()
            if not students:
                print("No students.")
            else:
                for s in students:
                    print(f"{s['id']}: {s['name']} (age {s['age']}, {s['grade_level']})")

        elif choice == "3":
            courses = get_all_courses()
            if not courses:
                print("No courses.")
            else:
                for c in courses:
                    print(f"{c['id']}: {c['course_name']} (Instructor: {c['instructor']})")

        elif choice == "4":
            try:
                s_name = _prompt_non_empty("Student name: ")
                c_name = _prompt_non_empty("Course name: ")
                students = find_student_by_name(s_name)
                if not students:
                    print("Student not found.")
                    continue
                courses = find_course_by_name(c_name)
                if not courses:
                    print("Course not found.")
                    continue
                # Disambiguate duplicates
                if len(students) > 1:
                    print("Multiple students found:")
                    for idx, s in enumerate(students, 1):
                        print(f"{idx}. {s['id']}: {s['name']} (age {s['age']}, {s['grade_level']})")
                    sel = _prompt_int("Select student #: ", min_val=1, max_val=len(students))
                    student_id = students[sel - 1]["id"]
                else:
                    student_id = students[0]["id"]

                if len(courses) > 1:
                    print("Multiple courses found:")
                    for idx, c in enumerate(courses, 1):
                        print(f"{idx}. {c['id']}: {c['course_name']} (Instructor: {c['instructor']})")
                    sel = _prompt_int("Select course #: ", min_val=1, max_val=len(courses))
                    course_id = courses[sel - 1]["id"]
                else:
                    course_id = courses[0]["id"]

                try:
                    enroll_student(student_id, course_id)
                    print("Enrolled.")
                except sqlite3.IntegrityError:
                    print("Already enrolled.")
            except EOFError:
                print("Input ended.")

        elif choice == "5":
            # Show roster for all courses without prompting
            courses = get_all_courses()
            if not courses:
                print("No courses.")
            else:
                for c in courses:
                    roster = get_course_roster(c['id'])
                    print(f"Roster for {c['course_name']} (Instructor: {c['instructor']}):")
                    if not roster:
                        print("- No students enrolled.")
                    else:
                        for r in roster:
                            print(f"- {r['student_id']}: {r['name']} ({r['grade_level']})")

        elif choice == "6":
            try:
                confirm = input("Type DELETE to erase students and enrollments: ").strip()
            except EOFError:
                print("Input ended.")
                continue
            if confirm == "DELETE":
                clear_all_data()
                print("Students and enrollments cleared.")
            else:
                print("Canceled.")

        elif choice == "7":
            print("Goodbye!")
            close_connection()
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()



