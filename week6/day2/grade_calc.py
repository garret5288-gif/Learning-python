# grade calculator that computes average, highest, lowest and letter grades

def collect_grades(): # Collect grades from user
    grades = [] # Initialize empty list for grades
    while True: # Loop to collect grades
        grade_input = input("Enter a grade (or 'done' to finish): ")
        if grade_input.lower() == 'done': # Check if user is done entering grades
            break
        try: # Try to convert input to float
            grade = float(grade_input)
            if 0 <= grade <= 100: # Validate grade range
                grades.append(grade) # Add valid grade to list
            else: # Handle invalid grade
                print("Please enter a grade between 0 and 100.")
        except ValueError: # Handle non-numeric input
            print("Invalid input. Please enter a numeric grade or 'done'.")
    return grades # Return the list of collected grades

def calculate_statistics(grades): # Calculate average, highest, lowest
    if not grades: # Check if grades list is empty
        return None, None, None
    average = sum(grades) / len(grades) # Calculate average
    highest = max(grades)
    lowest = min(grades)
    return average, highest, lowest

def letter_grade(score): # Convert numeric score to letter grade
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def main(): # Main function to run the grade calculator
    grades = collect_grades()
    average, highest, lowest = calculate_statistics(grades)
    if average is not None: # If there are grades, print statistics
        print(f"Average: {letter_grade(average)} ({average:.2f})")
        print(f"Highest: {letter_grade(highest)} ({highest})")
        print(f"Lowest: {letter_grade(lowest)} ({lowest})")
    else:
        print("No grades were entered.")

main() # Run the main function