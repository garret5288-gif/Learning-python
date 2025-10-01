# Student Database Management System
# This program manages a simple student database and allows users to view student information.

student_grades = { # Dictionary of student names and their grades
    "garret": {"Math": 92, 
               "Science": 85, 
               "History": 88, 
               "English": 90,
    },
    "alice": {"Math": 85, 
              "Science": 90, 
              "History": 87, 
              "English": 93,
    },
    "bob": {"Math": 78, 
            "Science": 82, 
            "History": 80, 
            "English": 85,
    },
    "brandon": {"Math": 89, 
                "Science": 94, 
                "History": 91, 
                "English": 88,
    },
    "daniel": {"Math": 92, 
               "Science": 85, 
               "History": 88, 
               "English": 90,
    },
}

def get_student_info(name): # Function to get student information
    for student, grades in student_grades.items(): # Iterate through students
        if student == name.lower(): # Match student name
            return grades
        elif name.lower() not in student_grades:
            return None # Student not found
    return None # Default return if not found
 
def display_student_info(name): # Function to display student information
    grade = get_student_info(name) # Get the student's grades
    if grade is None: # Check if student exists
        print("Student not found.")
        return # Exit if student not found
    # Calculate total, average, min, and max scores
    total = sum(grade.values()) # Total score calculation
    average = total / len(grade) # Average score calculation
    min_score = min(grade.values()) # Minimum score calculation
    max_score = max(grade.values()) # Maximum score calculation
    print(f"Grades for {name.capitalize()}:")
    for subject, score in grade.items(): # Display each subject and score
        print(f"  {subject}: {score}")
    print(f"  Min score: {min_score}")
    print(f"  Max score: {max_score}")
    print(f"  Average: {average:.2f}")

def main(): # Main function to run the student database
    print("Available students:")
    for student in student_grades.keys(): # List available students
        print(student.capitalize())
    while True: # Loop to allow multiple views
        name = input("Enter student name to view (or 'exit' to quit): ")
        if name.lower() == 'exit':
            print("Exiting the student database.")
            break # Exit condition
        elif not name: # Handle empty input
            print("Invalid input. Please enter a name.")
            continue
        display_student_info(name)

main()