import sqlite3
# Student Management System with Students, Grades, Attendance, and Courses
conn = sqlite3.connect("student_management.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()
# Create students table if not exists
cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL UNIQUE
)
''')
# Seed initial courses
PRESET_COURSES = ["Math", "Science", "English", "History", "Economics"]

def seed_courses():
    """Insert preset courses if they are not already present."""
    for name in PRESET_COURSES:
        cur.execute("SELECT 1 FROM courses WHERE course_name = ?", (name,))
        if not cur.fetchone():
            cur.execute("INSERT INTO courses (course_name) VALUES (?)", (name,))
    conn.commit()

def ensure_grades_schema():
    """Ensure the grades table has course_id for linking to courses (migrate if needed)."""
    cur.execute("PRAGMA table_info(grades)")
    cols = {row[1] for row in cur.fetchall()}
    if 'course_id' not in cols:
        # Add course_id column for existing databases
        cur.execute("ALTER TABLE grades ADD COLUMN course_id INTEGER")
        conn.commit()

def add_student(first_name: str, last_name: str):
    cur.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first_name.strip(), last_name.strip()))
    conn.commit()
    print(f"Added student: {first_name} {last_name}")

def attend_student(student_id: int, course_id: int, date: str, status: str):
    cur.execute("INSERT INTO attendance (student_id, course_id, date, status) VALUES (?, ?, ?, ?)", (student_id, course_id, date.strip(), status.strip()))
    conn.commit()
    print(f"Recorded attendance for student ID {student_id} in course ID {course_id} on {date} as {status}")


def add_grade_for_course(student_id: int, course_id: int, grade: int):
    cur.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
    conn.commit()
    print(f"Added grade {grade} for student ID {student_id} in course ID {course_id}")

def remove_student_by_id(student_id: int):
    """Remove a student and cascade delete their grades and attendance."""
    # Confirm exists
    cur.execute("SELECT first_name, last_name FROM students WHERE id = ?", (student_id,))
    row = cur.fetchone()
    if not row:
        print("Student not found.")
        return
    first_name, last_name = row
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print(f"Removed student: {first_name} {last_name}")

def list_grades(student_id: int):
    cur.execute('''
    SELECT g.id, c.course_name, g.grade
    FROM grades g
    JOIN courses c ON g.course_id = c.id
    WHERE g.student_id = ?
    ORDER BY c.course_name
    ''', (student_id,))
    rows = cur.fetchall()
    if not rows:
        print("No grades found for that student.")
    else:
        for row in rows:
            print(f"Grade ID: {row[0]}, Course: {row[1]}, Grade: {row[2]}")
        # Per-course averages
        cur.execute('''
        SELECT c.course_name, COUNT(g.grade) as cnt, AVG(g.grade) as avg_grade
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        WHERE g.student_id = ?
        GROUP BY c.course_name
        ORDER BY c.course_name
        ''', (student_id,))
        avg_rows = cur.fetchall()
        print("\nCourse Averages:")
        for cname, cnt, avg_grade in avg_rows:
            print(f"{cname}: {cnt} grades, Average: {avg_grade:.2f}")
        # Overall average
        cur.execute('SELECT COUNT(grade), AVG(grade) FROM grades WHERE student_id = ?', (student_id,))
        cnt_all, avg_all = cur.fetchone()
        if cnt_all:
            print(f"\nOverall: {cnt_all} grades, Average: {avg_all:.2f}")

def list_students():
    # Fetch students with overall average (if any grades)
    cur.execute('''
    SELECT s.id, s.first_name, s.last_name,
           COUNT(g.grade) as grade_count,
           AVG(g.grade) as avg_grade
    FROM students s
    LEFT JOIN grades g ON g.student_id = s.id
    GROUP BY s.id, s.first_name, s.last_name
    ORDER BY s.last_name, s.first_name
    ''')
    rows = cur.fetchall()
    if not rows:
        print("No students.")
        return
    for sid, first, last, grade_count, avg_grade in rows:
        if grade_count:
            print(f"ID: {sid}, Name: {first} {last}, Overall Avg: {avg_grade:.2f} ({grade_count} grades)")
        else:
            print(f"ID: {sid}, Name: {first} {last}, Overall Avg: N/A (0 grades)")

def list_courses():
    cur.execute("SELECT id, course_name FROM courses")
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Course Name: {row[1]}")

def find_students_by_name(name: str):
    """Case-insensitive search for students by full name (first last). Returns list of (id, first_name, last_name)."""
    needle = ' '.join(name.split()).lower()
    cur.execute("SELECT id, first_name, last_name FROM students WHERE lower(first_name || ' ' || last_name) = ?", (needle,))
    return cur.fetchall()

def find_courses_by_name(name: str):
    """Case-insensitive search for a course by name. Returns list of (id, course_name)."""
    needle = name.strip().lower()
    cur.execute("SELECT id, course_name FROM courses WHERE lower(course_name) = ?", (needle,))
    return cur.fetchall()

def _student_label(row) -> str:
    return f"ID {row[0]} - {row[1]} {row[2]}"

def _course_label(row) -> str:
    return f"ID {row[0]} - {row[1]}"

def choose_student_from_matches(rows):
    """Pick a student row (id, first_name, last_name) when multiple match."""
    if not rows:
        return None
    if len(rows) == 1:
        return rows[0]
    for idx, row in enumerate(rows, 1):
        print(f"{idx}. {_student_label(row)}")
    while True:
        sel = input("Select a number: ").strip()
        if sel.isdigit():
            i = int(sel)
            if 1 <= i <= len(rows):
                return rows[i-1]
        print("Invalid selection. Try again.")

def choose_course_from_matches(rows):
    """Pick a course row (id, course_name) when multiple match."""
    if not rows:
        return None
    if len(rows) == 1:
        return rows[0]
    for idx, row in enumerate(rows, 1):
        print(f"{idx}. {_course_label(row)}")
    while True:
        sel = input("Select a number: ").strip()
        if sel.isdigit():
            i = int(sel)
            if 1 <= i <= len(rows):
                return rows[i-1]
        print("Invalid selection. Try again.")

def list_attendance(student_id: int):
    cur.execute('''
    SELECT a.date, a.status, c.course_name
    FROM attendance a
    JOIN courses c ON a.course_id = c.id
    WHERE a.student_id = ?
    ORDER BY a.date
    ''', (student_id,))
    rows = cur.fetchall()
    for row in rows:
        print(f"Date: {row[0]}, Status: {row[1]}, Course: {row[2]}")

def menu():
    print("\nStudent Management System")
    print("1. Add Student")
    print("2. Record Attendance (all courses)")
    print("3. Add Grade (by Student & Course name)")
    print("4. Attendance Report (by Student name)")
    print("5. List Students")
    print("6. List Courses")
    print("7. List Grades for Student (by name)")
    print("8. Remove Student (by name)")
    print("9. Exit\n")

def main():
    try:
        # Seed preset courses on startup
        ensure_grades_schema()
        # Ensure attendance has course_id for per-course tracking
        cur.execute("PRAGMA table_info(attendance)")
        cols_att = {row[1] for row in cur.fetchall()}
        if 'course_id' not in cols_att:
            cur.execute("ALTER TABLE attendance ADD COLUMN course_id INTEGER")
            conn.commit()
        seed_courses()
        while True:
            menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                first_name = input("First Name: ").strip()
                last_name = input("Last Name: ").strip()
                add_student(first_name, last_name)
            elif choice == "2":
                student_name = input("Student name (First Last): ").strip()
                stu_matches = find_students_by_name(student_name)
                stu = choose_student_from_matches(stu_matches)
                if not stu:
                    print("No matching student found.")
                    continue
                # Loop through all courses and record attendance for each
                cur.execute("SELECT id, course_name FROM courses ORDER BY course_name")
                all_courses = cur.fetchall()
                if not all_courses:
                    print("No courses found.")
                    continue
                student_id = stu[0]
                date = input("Date (YYYY-MM-DD): ").strip()
                for course_id, course_name in all_courses:
                    while True:
                        status = input(f"Status for {course_name} (Present/Absent): ").strip()
                        status_norm = status.lower()
                        if status_norm in ("present", "absent"):
                            # Normalize casing
                            status_final = "Present" if status_norm == "present" else "Absent"
                            attend_student(student_id, course_id, date, status_final)
                            break
                        print("Please enter 'Present' or 'Absent'.")
            elif choice == "3":
                student_name = input("Student name (First Last): ").strip()
                stu_matches = find_students_by_name(student_name)
                stu = choose_student_from_matches(stu_matches)
                if not stu:
                    print("No matching student found.")
                    continue
                # Fetch all courses and prompt for a grade for each
                cur.execute("SELECT id, course_name FROM courses ORDER BY course_name")
                all_courses = cur.fetchall()
                if not all_courses:
                    print("No courses found.")
                    continue
                for course_id, course_name in all_courses:
                    while True:
                        raw = input(f"Enter grade (0-100) for {course_name}: ").strip()
                        if not raw.isdigit():
                            print("Please enter a valid integer between 0 and 100.")
                            continue
                        grade = int(raw)
                        if 0 <= grade <= 100:
                            add_grade_for_course(stu[0], course_id, grade)
                            break
                        print("Grade must be between 0 and 100.")
            elif choice == "4":
                student_name = input("Student name (First Last): ").strip()
                stu_matches = find_students_by_name(student_name)
                stu = choose_student_from_matches(stu_matches)
                if not stu:
                    print("No matching student found.")
                    continue
                list_attendance(stu[0])
            elif choice == "5":
                list_students()
            elif choice == "6":
                list_courses()
            elif choice == "7":
                student_name = input("Student name (First Last): ").strip()
                stu_matches = find_students_by_name(student_name)
                stu = choose_student_from_matches(stu_matches)
                if not stu:
                    print("No matching student found.")
                    continue
                list_grades(stu[0])
            elif choice == "8":
                student_name = input("Student name to remove (First Last): ").strip()
                stu_matches = find_students_by_name(student_name)
                stu = choose_student_from_matches(stu_matches)
                if not stu:
                    print("No matching student found.")
                    continue
                confirm = input(f"Are you sure you want to remove {_student_label(stu)}? (y/N): ").strip().lower()
                if confirm == 'y':
                    remove_student_by_id(stu[0])
                else:
                    print("Cancelled.")
            elif choice == "9":
                print("Exiting...")
                conn.close()
                break
            else:
                print("Invalid choice. Please try again.")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        try:
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()