# Multi-level Data Structure: School with Classes, Students, and Grades
# Displays student grades for selected classes or all classes

classes = { # Sample school data with classes, students, and their grades
    "Class1": {
        "Garret": {"Math": 90, "Science": 85, "English": 88},
        "Alice": {"Math": 92, "Science": 89, "English": 95},
        "Bob": {"Math": 78, "Science": 80, "English": 82},
        "Brandon": {"Math": 85, "Science": 87, "English": 90},
        "Daniel": {"Math": 88, "Science": 84, "English": 86},
    },
    "Class2": {
        "Eve": {"Math": 91, "Science": 90, "English": 93},
        "Frank": {"Math": 76, "Science": 79, "English": 81},
        "Grace": {"Math": 89, "Science": 88, "English": 90},
        "Hannah": {"Math": 94, "Science": 92, "English": 96},
        "Ivy": {"Math": 87, "Science": 85, "English": 88},
    },
    "Class3": {
        "Jack": {"Math": 82, "Science": 80, "English": 84},
        "Kathy": {"Math": 90, "Science": 91, "English": 92},
        "Liam": {"Math": 75, "Science": 78, "English": 80},
        "Mia": {"Math": 88, "Science": 86, "English": 89},
        "Noah": {"Math": 93, "Science": 94, "English": 95},
    }
}

def school_data(school): # Function to display data for the entire school or selected classes
    for class_name, students in school.items(): # Iterate through classes
        print(f"\n{class_name}:") # Print class name
        for student, grades in students.items(): # Iterate through students
            grades_str = ', '.join([f"{subject}: {score}" for subject, score in grades.items()]) # Format grades
            print(f"  {student}: {grades_str}")

def main(): # Main function to run the school data viewer
    print("School Data Viewer")
    print("===================")
    class_names = list(classes.keys()) # List of class names
    while True: # Loop to allow multiple views
        print("\nAvailable classes:")
        for i, class_name in enumerate(class_names, 1): # Display classes with numbers
            print(f"{i}. {class_name}") # Print each class
        print(f"{len(class_names)+1}. View all classes") # Option to view all classes
        print(f"{len(class_names)+2}. Exit")
        choice = input("Select a class to view or an option: ")
        if choice == str(len(class_names)+2): # Exit condition
            print("Exiting the school data viewer.")
            break
        elif choice == str(len(class_names)+1): # View all classes
            school_data(classes)
        elif choice.isdigit() and 1 <= int(choice) <= len(class_names): # Valid class choice
            selected_class = class_names[int(choice)-1] # Get selected class
            school_data({selected_class: classes[selected_class]})
        else: # Invalid choice
            print("Invalid option. Please try again.")

main()