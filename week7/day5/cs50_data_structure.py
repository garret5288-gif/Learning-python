
# Student lookup using dictionary methods and iteration.
# Parses data_structure.txt (name,age,grade)
# Lists student names
# Lets you choose by name or number to show age and grade


FILE_PATH = "/Users/garretadkins/Documents/GitHub/Learning-python/Learning-python/week7/day5/data_structure.txt"


def load_students(path: str) -> dict: 
    """Build a dict: name -> list of {age:int, grade:int} using iteration and setdefault."""
    students: dict[str, list[dict]] = {} # type hint for dict
    with open(path, "r") as f: # open the file for reading
        lines = f.read().splitlines()

    # Expect header: name,age,grade
    for i, line in enumerate(lines):  # iteration over lines
        if i == 0 or not line.strip():
            continue  # skip header/blank lines
        parts = line.split(",")
        if len(parts) != 3: # malformed line
            continue
        name, age, grade = parts[0].strip(), parts[1].strip(), parts[2].strip()
        students.setdefault(name, []).append({"age": int(age), "grade": int(grade)})
    return students


def list_students(students: dict) -> list[str]:
    names: list[str] = [] # type hint for list
    for name in students.keys():  # iteration over dict keys
        names.append(name) # add to list
    names.sort()
    return names


def lookup_student(students: dict, name: str) -> str:
    matches = students.get(name)  # dictionary get
    if not matches:  # no matches found
        return "Student not found"
    lines: list[str] = []
    for m in matches:  # iteration over possible duplicates
        lines.append(f"{name}: age={m['age']}, grade={m['grade']}")
    return "\n".join(lines)


def main(): # Main program loop
    students = load_students(FILE_PATH)
    names = list_students(students)

    if not names: # no students
        print("No students found.")
        return

    print("Student Data Lookup")
    print("-------------------")

    while True: # main loop
        print("\nStudents:")
        for i, n in enumerate(names, start=1):  # iteration to display menu
            print(f" {i}. {n}") # show number and name

        choice = input("\nType a student name or number (or 'exit'): ").strip()
        if choice.lower() == "exit": # exit the program
            break

        selected = None # reset selection
        if choice.isdigit(): # number chosen
            idx = int(choice) # convert to int
            if 1 <= idx <= len(names): # valid index
                selected = names[idx - 1]
        else:  # name chosen
            selected = choice

        print(lookup_student(students, selected))


if __name__ == "__main__":
    main()
