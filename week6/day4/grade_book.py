# Student Grade Book

students = ["john", "jane", "doe", "emily", "michael"]
grades = [[85, 92, 78, 88, 90], [82, 79, 88, 91, 87], [90, 85, 84, 92, 89], [76, 81, 79, 85, 80], [88, 90, 92, 94, 91]]

def average(grades): # Calculate average of a list of grades
    return sum(grades) / len(grades) if grades else 0 # Avoid division by zero

for i in range(len(students)): # Iterate through students and their grades
    print(f"{students[i]}: {grades[i]} - Average: {average(grades[i]):.1f}") # Print student name, grades, and average