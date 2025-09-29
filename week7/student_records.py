# Student Records System
# This program stores and retrieves student grades using a dictionary.

grades = { # Dictionary of student names and their grades
    "garret": {"Math": 95, "Science": 88, "History": 92},
    "alice": {"Math": 85, "Science": 90, "History": 87},
    "bob": {"Math": 78, "Science": 82, "History": 80},
    "brandon": {"Math": 89, "Science": 94, "History": 91}
}

def check_grades(): # Function to check and display grades
    print("Student Records System")
    print("=========================")
    print("Available students: Garret, Alice, Bob, Brandon")
    while True: # Loop to allow multiple queries
        name = input("Enter student name (or 'exit' to quit): ")
        if name.lower() == 'exit': # Exit condition
            print("Exiting the student records system.")
            break
        if not name: # Handle empty input
            print("Invalid input. Please enter a name.")
            continue
        student_grades = grades.get(name.lower())
        if student_grades:
            print(f"Grades for {name}:")
            for subject, score in student_grades.items():
                print(f"  {subject}: {score}")
        else:
            print("Student not found.")

check_grades()