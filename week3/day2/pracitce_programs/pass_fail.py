while True:
    grade_input = input("Enter your grade: ")
    if grade_input.isdigit():
        grade = int(grade_input)
        if 0 <= grade <= 100:
            break
        else:
            print("Invalid input. Please enter a grade between 0 and 100.")
    else:
        print("Invalid input. Please enter a numeric grade.")

if grade >= 60:
    print("You passed!")
else:
    print("You failed.")
