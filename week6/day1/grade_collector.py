# grade collector that collects grades until the user is done

def collect_grades():
    grades = [] # Initialize empty list for grades
    while True: # Loop to collect grades
        entry = input("Enter a grade (or type 'done' to finish): ")
        if entry.lower() == 'done' or entry == '':
            break
        try: # Try to convert input to float
            grade = float(entry)
            grades.append(grade)
        except ValueError: # Handle invalid input
            print("Please enter a valid number.")
    return grades # Return the list of collected grades

def main(): # Main function to run the grade collector
    grades = collect_grades()
    print("Grades collected:", grades)
    if grades: # If there are grades, print statistics
        print("Average:", sum(grades)/len(grades))
        print("Highest:", max(grades))
        print("Lowest:", min(grades))
# Run the main function
main()
