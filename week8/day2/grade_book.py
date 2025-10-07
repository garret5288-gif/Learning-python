def load_grades(filename):
    grades = []
    with open(filename, "r") as file:
        next(file)  # Skip header line
        for line in file:
            first_name, last_name, age, grade = line.strip().split(",")
            grades.append({
                "first_name": first_name,
                "last_name": last_name,
                "age": int(age),
                "grade": int(grade)
            })
    return grades

def average_grade(grades):
    if not grades:
        return 0
    total = sum(student["grade"] for student in grades)
    return total / len(grades)

def main():
    filename = "grades.csv"
    grades = load_grades(filename)
    avg = average_grade(grades)
    print(f"Average grade: {avg:.2f}")
    print(grades)

if __name__ == "__main__":
    main()