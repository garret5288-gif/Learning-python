# Student Grade Input and Average Calculation
# Collect student names and their grades, then display each student's average grade

def add_student(): # Function to add a student and their grades
    student = []
    grades = []

    name = input("Enter student name: ")
    student.append(name) # Add name to student list
    while True: # Loop to collect grades
        grade_input = input(f"Enter the grades for {name} or 'done' to finish: ")
        if grade_input.lower() == 'done': # Check if user is done entering grades
            break
        try:
            grade = float(grade_input) # Convert input to float
            grades.append(grade) # Add grade to grades list
        except ValueError:
            print("Invalid input. Please enter a numeric grade.")
    return student, grades

def average(grades):
    if not grades:
        return 0
    return sum(grades) / len(grades)


def main():
    students = []
    all_grades = []

    while True:
        student, grades = add_student()
        if student and grades:
            students.extend(student)
            all_grades.append(grades)
        cont = input("Add another student? (y/n): ") # Ask if user wants to add another student
        if cont.lower() != 'y': # Exit loop if user does not want to continue
            break
    print("\nStudent Grades:")
    for i in range(len(students)): # Iterate through students and their grades
        print(f"{students[i]}: {all_grades[i]} - Average: {average(all_grades[i]):.1f}") # Print student name, grades, and average

main() # Run the main function

