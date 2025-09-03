score = input("Enter your score: ").strip()

if not score.isdigit():
    print("Invalid input. Please enter a valid number.")
else:
    score = int(score.strip())
    if 97 <= score <= 100:
        print("Grade: A+")
    elif 93 <= score <= 96:
        print("Grade: A")
    elif 90 <= score <= 93:
        print("Grade: A-")
    elif 87 <= score <= 89:
        print("Grade: B+")
    elif 83 <= score <= 86:
        print("Grade: B")
    elif 80 <= score <= 82:
        print("Grade: B-")
    elif 77 <= score <= 79:
        print("Grade: C+")
    elif 73 <= score <= 76:
        print("Grade: C")
    elif 70 <= score <= 72:
        print("Grade: C-")
    elif 67 <= score <= 69:
        print("Grade: D+")
    elif 63 <= score <= 66:
        print("Grade: D")
    elif 60 <= score <= 62:
        print("Grade: D-")
    elif 0 <= score < 60:
        print("Grade: F")
    else:
        print("Invalid score.")
