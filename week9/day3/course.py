from student import Student # Import Student class
# Course class to manage students

class Course: # Course class to manage students
    def __init__(self, course_name: str):
        self.course_name = course_name
        self.students: list[Student] = []

    def add_student(self, student: Student): # Add a student to the course
        if any(s.student_id == student.student_id for s in self.students):
            print(f"{student.name} is already in {self.course_name}.")
            return
        self.students.append(student) # Add student to the course
        student.enroll(self.course_name)
        print(f"Added student {student.name} to {self.course_name}.")

    def list_students(self): # List all students in the course
        if not self.students:
            print("No students enrolled.")
            return # no students
        print(f"Students in {self.course_name}:")
        for s in self.students: # display each student
            s.display_info()
    
    def find_student(self, student_id): # Find student by ID
        for s in self.students: # search each student
            if s.student_id == student_id:
                return s # found student
        return None
    
    def remove_student(self, student_id): # Remove student by ID
        s = self.find_student(student_id)
        if not s: # student not found
            print(f"Student {student_id} not found in {self.course_name}.")
            return
        self.students = [st for st in self.students if st.student_id != student_id]
        s.drop(self.course_name) # update student's courses
        print(f"Removed student {s.name} from {self.course_name}.")

def menu(): # Display menu options
    print("\nSchool Course Menu:")
    print("1. List students and their courses")
    print("2. List courses and their students")
    print("3. Enroll student in a course")
    print("4. Exit")

courses = [Course("Math"), 
           Course("History"),
           Course("Science")]
students = [Student("Alice", 1),
            Student("Bob", 2),
            Student("Charlie", 3)]

# --- Helpers ---
def get_course(name):
    for c in courses:
        if c.course_name.lower() == name.lower():
            return c
    return None

def get_student(sid): # Get student by ID
    for s in students:
        if s.student_id == sid:
            return s
    return None

def list_students_with_courses(): # List all students with their courses
    if not students:
        print("No students available.")
        return
    print("Students and their courses:")
    for s in students: # display each student
        enrolled = ", ".join(s.courses) if getattr(s, 'courses', None) else "(none)"
        print(f" - {s.name} (ID {s.student_id}): {enrolled}")

def list_courses_with_students(): # List all courses with their students
    if not courses: # no courses
        print("No courses available.")
        return
    for c in courses: # display each course
        print(f"\nCourse: {c.course_name}")
        if not c.students:
            print("  (no students)")
        else: # display each student
            for st in c.students:
                print(f"  - {st.name} (ID {st.student_id})")

def main(): # Main program loop
    while True:
        menu()
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            list_students_with_courses()
        elif choice == "2":
            list_courses_with_students()
        elif choice == "3":
            try:
                sid = int(input("Enter student ID: ").strip())
            except ValueError:
                print("Invalid student ID.")
                continue
            course_name = input("Enter course name: ").strip()
            if not course_name:
                print("Course name cannot be empty.")
                continue
            s = get_student(sid)
            c = get_course(course_name)
            if not s:
                print("Student not found.")
                continue
            if not c:
                print("Course not found.")
                continue
            c.add_student(s)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()