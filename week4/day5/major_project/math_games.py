# A simple math games program with addition, subtraction, and multiplication quizzes.
# The user can choose a game, answer 10 questions, and receive a score at the end.
import random # Import random module for generating random numbers

def main(): # Define main function
    
    while True: # Main loop to display menu and handle user choice
        print("Welcome to Math Games!")
        print("1. Addition Quiz")
        print("2. Subtraction Quiz")
        print("3. Multiplication Quiz")
        print("4. Exit")

        choice = input("Choose a game (1-4): ") # Prompt user for game choice
        if choice == '1':
            quiz("addition")
        elif choice == '2':
            quiz("subtraction")
        elif choice == '3':
            quiz("multiplication")
        elif choice == '4': # Exit option
            print("Thanks for playing!")
            break
        else: # Handle invalid input
            print("Invalid choice. Please select a number between 1 and 4.")

def quiz(operation): # Define quiz function
    score = 0
    for i in range(10): # Ask 10 questions
        a = random.randint(1, 10) # Generate random number between 1 and 10
        b = random.randint(1, 10)
        if operation == "addition":
            while True:
                user_input = input(f"What is {a} + {b}? ") # Prompt user for answer 
                try: # Try to convert input to integer
                    answer = int(user_input)
                    break
                except ValueError: # Handle non-integer input
                    print("Please enter a valid integer.")
            if answer == a + b:
                print("Correct!")
                score += 1 # Increment score for correct answer
            else:
                print(f"Wrong! The correct answer is {a + b}.") # Provide correct answer
        elif operation == "subtraction":
            while True:
                user_input = input(f"What is {a} - {b}? ")
                try:
                    answer = int(user_input)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
            if answer == a - b:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer is {a - b}.")
        elif operation == "multiplication":
            while True:
                user_input = input(f"What is {a} * {b}? ")
                try:
                    answer = int(user_input)
                    break
                except ValueError:
                    print("Please enter a valid integer.")
            if answer == a * b:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer is {a * b}.")
    print(f"Your score: {score}/10") # Display user's score
    print()
   
main() # Call main function to start the program
