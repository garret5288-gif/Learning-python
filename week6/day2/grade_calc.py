def collect_grades():
    grades = []
    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ")
        if grade_input.lower() == 'done':
            break
        try:
            grade = float(grade_input)
            if 0 <= grade <= 100:
                grades.append(grade)
            else:
                print("Please enter a grade between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric grade or 'done'.")
    return grades

def calculate_statistics(grades):
    if not grades:
        return None, None, None
    average = sum(grades) / len(grades)
    highest = max(grades)
    lowest = min(grades)
    return average, highest, lowest

def letter_grade(score):
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

def main():
    grades = collect_grades()
    average, highest, lowest = calculate_statistics(grades)
    if average is not None:
        print(f"Average: {letter_grade(average)} ({average:.2f})")
        print(f"Highest: {letter_grade(highest)} ({highest})")
        print(f"Lowest: {letter_grade(lowest)} ({lowest})")
    else:
        print("No grades were entered.")

main()