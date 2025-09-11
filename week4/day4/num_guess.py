# A simple number guessing game
import random
# Generate a random number between 1 and 100
answer = random.randint(1, 100)
attempts = 0

while True:
    guess = input("Enter a number between 1 and 100 or type 'exit' to quit: ").strip()
    if guess == "": # Check for empty input
        print("Input cannot be empty, please try again.")
    elif guess.lower() == "exit": # Check for exit command
        print("Thanks for playing!")
        break
    elif not guess.isdigit(): # Validate input
        print("Invalid input, please enter a valid number.")
    
    else:
        guess = int(guess) # Convert input to integer
        attempts += 1 # Increment attempt count
        if guess < 1 or guess > 100: # Check if guess is within range
            print("Enter number within the range of 1 to 100.")
        elif guess < answer: # Check if guess is lower than answer
            print("Guess higher! ")
        elif guess > answer: # Check if guess is higher than answer
            print("Guess lower!")
        else:
            print(f"Awesome! You've guessed the number {answer} in {attempts} attempts.")
            break