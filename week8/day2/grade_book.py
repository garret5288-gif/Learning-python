from pathlib import Path # for file paths
import csv # for CSV handling

DATA_FILE = Path("grades.csv") # default data file

def load_data(path: Path = DATA_FILE) -> list[dict]: # Load student data from CSV
    if not path.exists() or path.stat().st_size == 0: # no file or empty
        return []
    students = []
    with open(path, newline="") as f: # open for reading
        for row in csv.DictReader(f):
            raw = row.get("grades", "").strip()
            grades = []
            if raw: # parse grades if present
                for g in raw.split("|"): # split by |
                    try: grades.append(int(g)) # convert to int
                    except ValueError: pass
            students.append({"first_name": row.get("first_name",""), "last_name": row.get("last_name",""), "grades": grades})
    return students

def save_data(students: list[dict], path: Path = DATA_FILE) -> None: # Save student data to CSV
    with open(path, "w", newline="") as f: # open for writing
        fieldnames = ["first_name","last_name","grades"]
        writer = csv.DictWriter(f, fieldnames=fieldnames) # create writer
        writer.writeheader() # write header
        for s in students: # write each student
            writer.writerow({
                "first_name": s["first_name"],
                "last_name": s["last_name"],
                "grades": "|".join(str(g) for g in s.get("grades", []))
            })

def add_student(students: list[dict]): # Add a new student
    fn = input("First name: ").strip()
    ln = input("Last name: ").strip()
    students.append({"first_name": fn, "last_name": ln, "grades": []})
    print("Student added.\n")

def _choose_index(students: list[dict]): # Helper to choose student index
    for i, s in enumerate(students, 1): # display numbered list
        print(f"{i}) {s['first_name']} {s['last_name']}")
    choice = input("Select student number (blank cancels): ").strip()
    if not choice: return None # cancelled
    if not choice.isdigit(): return None # invalid
    idx = int(choice)-1 # convert to 0-based
    if not (0 <= idx < len(students)): return None
    return idx

def add_grade(students: list[dict]): # Add grade to existing student
    if not students: # No students yet
        print("No students yet.\n"); return
    idx = _choose_index(students)
    if idx is None: # cancelled
        print("Cancelled.\n"); return
    st = students[idx]
    while True: # loop to add grades
        raw = input("Grade (0-100, blank done): ").strip()
        if not raw: break
        try: # convert to int and validate
            g = int(raw)
            if 0 <= g <= 100:
                st['grades'].append(g); print("Added.")
            else:
                print("Range 0-100.")
        except ValueError: # invalid input
            print("Enter number.")
    print()

def list_students(students: list[dict]): # List all students with averages
    if not students:
        print("No students loaded.\n"); return
    for s in students: # display each student
        g = s.get('grades', [])
        avg = round(sum(g)/len(g),2) if g else 0
        print(f"{s['first_name']} {s['last_name']}: grades={g} avg={avg}")
    print()

def average_all(students: list[dict]) -> float: # Compute overall average
    g = [n for s in students for n in s.get('grades', [])]
    return sum(g)/len(g) if g else 0.0

def menu(): # Display menu options
    print("\nStudent Grade Book")
    print("1) Add student")
    print("2) Add grade to student")
    print("3) List students")
    print("4) Show overall average")
    print("5) Save")
    print("6) Load")
    print("7) Exit")

def main(): # Main program loop
    students = load_data()  # auto-load if file exists
    while True:
        menu()
        choice = input("Choose: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            add_grade(students)
        elif choice == "3":
            list_students(students)
        elif choice == "4":
            avg = average_all(students)
            print(f"Overall average: {avg:.2f}\n")
        elif choice == "5":
            save_data(students)
            print(f"Saved to {DATA_FILE.name}.\n")
        elif choice == "6":
            students = load_data()
            print(f"Loaded {len(students)} students.\n")
        elif choice == "7": # exit
            save_first = input("Save before exit? (y/N): ").strip().lower()
            if save_first.startswith('y'):
                save_data(students)
                print("Saved.")
            print("Goodbye.")
            break
        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    main()