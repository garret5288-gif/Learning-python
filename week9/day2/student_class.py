# student class with methods to add grades, calculate average and GPA
# interactive menu to add grades, show average and GPA
# input validation for grades (0-100)

class Student: # Define Student class
    def __init__ (self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.grades: list[int] = []

    def add_grade(self, grade: int): # Add a grade with validation
        if 0 <= grade <= 100:
            self.grades.append(grade)
        else:
            print("Grade must be between 0 and 100.")

    def average_grade(self): # Calculate average grade
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def grade_to_gpa(self, score: int) -> float:
        # Common 4.0 scale threshold mapping from percentage
        if score >= 93:   return 4.0   # A
        if score >= 90:   return 3.7   # A-
        if score >= 87:   return 3.3   # B+
        if score >= 83:   return 3.0   # B
        if score >= 80:   return 2.7   # B-
        if score >= 77:   return 2.3   # C+
        if score >= 73:   return 2.0   # C
        if score >= 70:   return 1.7   # C-
        if score >= 67:   return 1.3   # D+
        if score >= 63:   return 1.0   # D
        if score >= 60:   return 0.7   # D-
        return 0.0                     # F

    def calculate_gpa(self) -> float: # Calculate GPA
        """Return unweighted GPA (4.0 scale) from numeric grades.
        If there are no grades, returns 0.0.
        """
        if not self.grades: # no grades
            return 0.0
        total_points = sum(self.grade_to_gpa(g) for g in self.grades)
        gpa = total_points / len(self.grades)
        return round(gpa, 2)
    
def menu(): # Display menu options
    print("\nStudent grades")
    print("1. Add grade")
    print("2. Get average")
    print("3. Get GPA")
    print("4. Exit")

def main(): # Main program loop
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    student = Student(first_name, last_name)
    
    while True: # Loop until user chooses to exit
        menu()
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            raw = input("Enter grade (0-100, blank to cancel): ").strip()
            if raw == "":
                print("Add grade canceled.")
            else:
                try: # convert to int and validate
                    grade = int(raw)
                except ValueError:
                    print("Invalid grade. Please enter a number between 0 and 100.")
                else:
                    student.add_grade(grade)
                    print(f"Grade {grade} added.")
        elif choice == "2":
            avg = student.average_grade()
            print(f"Average grade: {avg:.2f}")
        elif choice == "3":
            gpa = student.calculate_gpa()
            print(f"GPA: {gpa:.2f}")
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()

