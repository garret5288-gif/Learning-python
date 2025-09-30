# Grade Analyzer

students_grades = { # Dictionary of student names and their grades
    "garret": {"Math": 95, "Science": 88, "History": 92},
    "alice": {"Math": 85, "Science": 90, "History": 87},
    "bob": {"Math": 78, "Science": 82, "History": 80},
    "brandon": {"Math": 89, "Science": 94, "History": 91},
    "daniel": {"Math": 92, "Science": 85, "History": 88}
}

def analyze_grades(): # Function to analyze and display grades
    print("Grade Analyzer")
    print("=========================")
    for student in students_grades.keys(): # List available students
        print(student.capitalize())
    while True: # Loop to allow multiple analyses
            name = input("Enter student name to analyze (or 'exit' to quit): ")
            if name.lower() == 'exit': # Exit condition
                print("Exiting the grade analyzer.")
                break
            elif not name: # Handle empty input
                print("Invalid input. Please enter a name.")
                continue
            elif name.lower() not in students_grades: # Handle unknown student
                print("Student not found. Please enter a valid student name.")
                continue
            student_grades = students_grades[name.lower()] # Get the student's grades
            total = sum(student_grades.values()) # Calculate total score
            average = total / len(student_grades) # Calculate average score
            min_score = min(student_grades.values())
            max_score = max(student_grades.values())
            print(f"Grades for {name.capitalize()}:")
            for subject, score in student_grades.items(): # Display each subject and score
                print(f"  {subject}: {score}")
            print(f"  Min score: {min_score}") # Display minimum score
            print(f"  Max score: {max_score}") # Display maximum score
            print(f"  Average: {average:.2f}") # Display average score

analyze_grades()