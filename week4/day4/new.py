import random

score = 0

def add():
    global score
    num1 = get_random_number()
    num2 = get_random_number()
    print(f"What is {num1} + {num2}?")
    user_answer = get_number()
    correct_answer = num1 + num2
    if user_answer == correct_answer:
        print("Correct!")
        score += 1
    else:
        print(f"Wrong! The correct answer is {correct_answer}.")

def subtract():
    global score
    num1 = get_random_number()
    num2 = get_random_number()
    print(f"What is {num1} - {num2}?")
    user_answer = get_number()
    correct_answer = num1 - num2
    if user_answer == correct_answer:
        print("Correct!")
        score += 1
    else:
        print(f"Wrong! The correct answer is {correct_answer}.")

def multiply():
    global score
    num1 = get_random_number()
    num2 = get_random_number()
    print(f"What is {num1} * {num2}?")
    user_answer = get_number()
    correct_answer = num1 * num2
    if user_answer == correct_answer:
        print("Correct!")
        score += 1
    else:
        print(f"Wrong! The correct answer is {correct_answer}.")

def main():
    print("Math games!")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Exit")

def get_choice():
    choice = input("Enter your choice (1-4): ")
    return choice

def get_number():
    return float(input("Enter a number: "))

def get_random_number():
    return random.randint(1, 50)

while True:

    score = 0

    main()
    choice = get_choice()
    if choice == "1":
        add()
    elif choice == "2":
        subtract()
    elif choice == "3":
        multiply()
    elif choice == "4":
        print(f"Your final score is {score}. Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")
    print(f"Your current score is {score}.\n")