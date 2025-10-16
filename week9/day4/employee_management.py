# Employee Management System
# This program defines an Employee class with attributes and methods to manage employee data.
import json # for data persistence
import os # for file operations
from typing import Optional # for type hints

DATA_FILE = "employees.json"


class Employee: # Employee class with attributes and methods
    count = 0 # class variable to track number of employees
    
    def __init__ (self, name, emp_id, position): # constructor
        self.name = name
        self.emp_id = emp_id
        self.position = position
        Employee.count += 1

    @classmethod # class method to get employee count
    def get_employee_count(cls):
        return cls.count

    def display_info(self): # display employee details
        print(f"Employee Name: {self.name}, ID: {self.emp_id}, Position: {self.position}")

    # Serialization helpers
    def to_dict(self):
        return {"name": self.name, "emp_id": self.emp_id, "position": self.position}

    @staticmethod
    def save_to_file(employees_list, path: str): # Save list of employees to JSON file
        try:
            data = [e.to_dict() for e in employees_list]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"Failed to save employees: {e}")

def get_employee_by_id(emp_id: int): # find employee by ID
    for e in employees:  # iterate through employee list
        if e.emp_id == emp_id:
            return e
    return None

def add_employee(name: str, emp_id: int, position: str):
    # prevent duplicate IDs
    if get_employee_by_id(emp_id):
        print(f"Employee ID {emp_id} already exists.")
        return
    new_employee = Employee(name, emp_id, position) # create new employee
    employees.append(new_employee) # add to list
    print(f"Added Employee: {name}, ID: {emp_id}, Position: {position}")
    save_employees()

def remove_employee(emp_id: int): # remove employee by ID
    global employees # modify global list
    before = len(employees) # count before removal
    employees = [emp for emp in employees if emp.emp_id != emp_id]
    removed = before - len(employees)
    if removed > 0: # if any employee was removed
        Employee.count -= removed # update count
        print(f"Removed Employee with ID: {emp_id}")
    else:
        print(f"No employee found with ID: {emp_id}")
    if removed: # only save if something was removed
        save_employees()

def update_employee(emp_id: int, new_name: Optional[str] = None, new_position: Optional[str] = None):
    emp = get_employee_by_id(emp_id) # find employee
    if not emp: # if employee not found
        print(f"No employee found with ID: {emp_id}")
        return
    if new_name: 
        emp.name = new_name
    if new_position:
        emp.position = new_position
    print(f"Updated Employee {emp.emp_id}: Name='{emp.name}', Position='{emp.position}'")
    save_employees() # save changes


def save_employees(path: str = DATA_FILE): # Save employee data to JSON file
    Employee.save_to_file(employees, path)

def load_employees(path: str = DATA_FILE): # Load employee data from JSON file
    global employees # modify global list
    if not os.path.exists(path):
        return False
    try: # attempt to load employee data
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        employees = []
        Employee.count = 0
        for item in data:
            name = str(item.get("name", "")).strip()
            position = str(item.get("position", "")).strip()
            try:
                emp_id = int(item.get("emp_id"))
            except (TypeError, ValueError):
                continue
            employees.append(Employee(name, emp_id, position))
        return True
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to load employees: {e}")
        return False

employees = []  # list to store employee instances

# Load from disk if available; otherwise create defaults
if not load_employees():
    employees = [
        Employee("Alice", 101, "Developer"),
        Employee("Bob", 102, "Designer"),
        Employee("Charlie", 103, "Manager"),
        Employee("Diana", 104, "Tester"),
        Employee("Ethan", 105, "Support")
    ]
    # Save initial defaults for persistence
    save_employees()

def menu(): # Display menu options
    print("\nEmployee Management System")
    print("1. List all employees")
    print("2. Add a new employee")
    print("3. Remove an employee")
    print("4. Show total number of employees")
    print("5. Update an employee")
    print("6. Exit")

def main(): # Main program loop
    while True:
        menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == '1':
            if not employees:
                print("No employees to display.")
            else:
                for emp in employees:
                    emp.display_info()
        elif choice == '2':
            name = input("Enter employee name: ").strip()
            emp_id_raw = input("Enter employee ID: ").strip()
            position = input("Enter employee position: ").strip()
            if not name or not emp_id_raw or not position:
                print("All fields are required.")
                continue
            try:
                emp_id = int(emp_id_raw)
            except ValueError:
                print("Employee ID must be a number.")
                continue
            add_employee(name, emp_id, position)
        elif choice == '3':
            emp_id_raw = input("Enter employee ID to remove: ").strip()
            try:
                emp_id = int(emp_id_raw)
            except ValueError:
                print("Employee ID must be a number.")
                continue
            remove_employee(emp_id)
        elif choice == '4':
            print(f"Total Employees: {Employee.get_employee_count()}")
        elif choice == '5':
            emp_id_raw = input("Enter employee ID to update: ").strip()
            try:
                emp_id = int(emp_id_raw)
            except ValueError:
                print("Employee ID must be a number.")
                continue
            new_name = input("New name (leave blank to keep): ").strip()
            new_position = input("New position (leave blank to keep): ").strip()
            update_employee(emp_id, new_name or None, new_position or None)
        elif choice == '6':
            print("Exiting Employee Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()