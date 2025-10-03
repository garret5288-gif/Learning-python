# Student Management System (menu-driven)
from __future__ import annotations # for Python 3.10 compatibility

import json # for JSON handling
from pathlib import Path # for file paths
from typing import Dict, List # for type hints

DATA_FILE = Path(__file__).with_suffix(".json")  # student_management_syst.json
ALLOWED_CLASSES = ["Math", "Science", "English", "History"] # fixed set of classes

def load_db() -> Dict: # Load or initialize the database
    # If file exists, load it; otherwise return empty structure
	if DATA_FILE.exists(): # file exists
		try: # try to load JSON
			db = json.loads(DATA_FILE.read_text())
			# Migrate student keys to lowercase for consistent lookups
			migrate_names_to_lowercase(db)
			return db
		except json.JSONDecodeError: # invalid JSON
			pass
	# structure: { students: { name: { classes: { class_name: [grades...] } } } }
	return {"students": {}}

def save_db(db: Dict) -> None: # Save the database to file
	DATA_FILE.write_text(json.dumps(db, indent=2))

def ensure_student(db: Dict, name: str) -> None: # Ensure student exists
	name = normalize_name(name) # normalize name
	students = db["students"] 
	if name not in students: # add if missing
		students[name] = {"classes": {}} # initialize class structure
	# Ensure fixed set of classes always exist
	classes = students[name]["classes"]
	for cls in ALLOWED_CLASSES: # fixed set of classes
		classes.setdefault(cls, [])

def add_grade(db: Dict, name: str, class_name: str, grade: float) -> None: # Add a grade to a student/class
	name = normalize_name(name)
	class_name = normalize_class(class_name)
	if class_name not in ALLOWED_CLASSES: 
		return
	ensure_student(db, name) # ensure student exists
	classes = db["students"][name]["classes"] # get classes dict
	classes.setdefault(class_name, []) # ensure class list exists
	classes[class_name].append(float(grade)) # add the grade

def add_grades_all_subjects(db: Dict, name: str) -> None:
	"""Prompt to add multiple grades for each fixed subject in one flow.
	Requires an existing student; does not auto-create.
	"""
	name = normalize_name(name)
	if name not in db["students"]: # Check if student exists
		print("Student not found.")
		return
	print(f"\nAdding grades for {name} (leave blank to skip a subject)")
	for cls in ALLOWED_CLASSES: 
		existing = db["students"][name]["classes"].get(cls, [])
		print(f"\nSubject: {cls}")
		print(f"Current grades: {existing}")
		line = input("Enter grades (comma-separated, blank to skip): ").strip()
		if not line: # Skip if no input
			continue
		# allow comma or space separated
		tokens = line.replace(",", " ").split()
		added = 0
		for t in tokens:
			try: # convert to float
				g = float(t)
			except ValueError: # invalid input
				print(f"  Skipped invalid grade: {t}")
				continue
			add_grade(db, name, cls, g) # add the grade
			added += 1
		print(f"  Added {added} grade(s) to {cls}.")

	# Auto-save after processing all subjects for this student
	save_db(db)

def update_grade(db: Dict, name: str, class_name: str, index: int, new_grade: float) -> bool:
	name = normalize_name(name)
	class_name = normalize_class(class_name)
	try: # try to update
        # Validate student, class, and index
		if class_name not in ALLOWED_CLASSES:
			return False # invalid class
		db["students"][name]["classes"][class_name][index] = float(new_grade)
		return True # success
	except (KeyError, IndexError):
		return False

def list_students(db: Dict) -> List[str]: # Return sorted list of student names
	return sorted(db["students"].keys())

def print_report(db: Dict) -> None: # Print report of all students and their average grades
	print("\n=== Student Report ===")
	for name in list_students(db):
		print(f"\n{name}")
		classes = db["students"][name]["classes"]
		if not classes: # no classes
			print("  (no classes)")
			continue
		# Only show allowed classes in a consistent order
		for cls in ALLOWED_CLASSES:
			grades = classes.get(cls, []) # get grades or empty list
			avg = round(sum(grades) / len(grades), 2) if grades else 0
			print(f"  {cls}: grades={grades} avg={avg}")

def show_student_grades(db: Dict, name: str) -> None:
	"""Print all subjects and enumerate grade indices for the given student."""
	student = db["students"].get(name)
	if not student:
		print("Student not found.")
		return
	classes = student["classes"]
	print(f"\nGrades for {name}:")
	for cls in ALLOWED_CLASSES: # fixed order
		grades = classes.get(cls, [])
		if not grades: # no grades
			print(f"  {cls}: (no grades)")
		else: # show indexed grades
			indexed = ", ".join(f"{i}:{g}" for i, g in enumerate(grades))
			print(f"  {cls}: {indexed}")

def normalize_class(value: str) -> str:
	# Normalize input to Title case and validate later
	return (value or "").strip().title()

def normalize_name(value: str) -> str:
	# Lowercase names for consistent storage and lookup
	return (value or "").strip().lower()

def migrate_names_to_lowercase(db: Dict) -> None:
	"""Convert all student keys to lowercase, merging classes if duplicates exist."""
	students = db.get("students", {})
	if not isinstance(students, dict):
		db["students"] = {}
		return
	new_map: Dict[str, Dict] = {}
	for key, val in students.items():
		nk = normalize_name(key)
		if nk not in new_map:
			new_map[nk] = val if isinstance(val, dict) else {"classes": {}}
		else:
			# merge classes
			existing_classes = new_map[nk].setdefault("classes", {})
			more_classes = (val or {}).get("classes", {}) if isinstance(val, dict) else {}
			for cls, grades in more_classes.items():
				existing_classes.setdefault(cls, [])
				if isinstance(grades, list):
					existing_classes[cls].extend(grades)
	db["students"] = new_map
	# Ensure fixed classes exist for each student
	for n in list(new_map.keys()):
		ensure_student(db, n)

def choose_class() -> str | None: # Prompt user to choose a class from allowed list
	print("Choose a class:")
	for i, cls in enumerate(ALLOWED_CLASSES, start=1):
		print(f" {i}) {cls}") # display options
	choice = input("Class number (or blank to cancel): ").strip()
	if not choice: # user cancelled
		return None
	if choice.isdigit(): # valid number
		idx = int(choice)
		if 1 <= idx <= len(ALLOWED_CLASSES):
			return ALLOWED_CLASSES[idx - 1]
	print("Invalid choice.")
	return None

def menu(): # Display menu options
	print("\nStudent Management System")
	print("1) Add student")
	print("2) Add grades to all subjects")
	print("3) Update a grade")
	print("4) List students")
	print("5) Show report")
	print("6) Save")
	print("7) Clear all data")
	print("8) Exit")

def main(): # Main program loop
	import sys
	db = load_db()

	while True: # main loop
		menu()
		choice = input("Choose: ").strip()
		if choice == "1":
			# Keep asking for student names until blank
			while True:
				name = normalize_name(input("Student name (blank to stop): "))
				if not name: # user cancelled
					break
				ensure_student(db, name)
				print(f"Added: {name}")
				save_db(db) # auto-save after each new student
		elif choice == "2": # Add grades to all subjects for a student
			name = normalize_name(input("Student name: "))
			if not name or name not in db["students"]:
				print("Student not found.")
				continue
			add_grades_all_subjects(db, name)
		elif choice == "3": # Update a specific grade
			name = normalize_name(input("Student name: "))
			if name not in db["students"]: # Check if student exists
				print("Student not found.")
				continue
			# Show all grades with indices to aid selection
			show_student_grades(db, name)
			cls = choose_class()
			if not cls: # user cancelled
				continue
			# Show current selected class grades again with indices
			sel_grades = db["students"][name]["classes"].get(cls, [])
			if sel_grades: # show if any grades exist
				print("Current indexes for", cls, ":", ", ".join(f"{i}:{g}" for i, g in enumerate(sel_grades)))
			else: # no grades
				print(f"No grades yet for {cls}.")
			try: # get index and new grade
				idx = int(input("Grade index (starting at 0): ").strip())
				new_grade = float(input("New grade: ").strip())
			except ValueError: # invalid input
				print("Invalid input.")
				continue
			if update_grade(db, name, cls, idx, new_grade):
				print("Updated.") # success
				save_db(db) # auto-save after successful update
			else: # update failed
				print("Update failed. Check name/class/index.")
		elif choice == "4": # List students
			print("Students:")
			for s in list_students(db):
				print("-", s)
		elif choice == "5": # Show report
			print_report(db)
		elif choice == "6": # Save database
			save_db(db)
			print(f"Saved to {DATA_FILE.name}")
		elif choice == "7": # Clear all data
			confirm = input("Type YES to confirm clearing all data: ").strip()
			if confirm == "YES":
				db["students"] = {}
				save_db(db)
				print("All data cleared.")
			else: # user cancelled
				print("Cancelled.")
		elif choice == "8": # Exit
			save_db(db)
			print("Goodbye.")
			break 
		else: # invalid choice
			print("Invalid choice.")

if __name__ == "__main__":
	main()

