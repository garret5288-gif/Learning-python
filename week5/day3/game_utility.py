import random # For dice rolling

def play_dice_game(): # Play a simple dice rolling game
    print("Welcome to the Dice Rolling Game!")
    score = 0 # Initialize score
    rounds = 0 # Initialize rounds
    sides = 10 # Initialize dice sides
    while True: # Game loop
        user_input = input("Roll the dice? (y/n): ").strip().lower()
        if user_input == 'y':
            roll = roll_dice(sides)
            print(f"You rolled a {roll}!")
            score += roll
            rounds += 1
            print(f"Current score: {score} after {rounds} rolls.")
        elif user_input == 'n':
            print(f"Game over! Final score: {score} in {rounds} rolls.")
            break # Exit the game
        else:
            print("Please enter 'y' or 'n'.")


def roll_dice(sides): # Roll a dice with given sides
    return random.randint(1, sides)

def calculate_score(rolls): # Calculate total score from rolls
    return sum(rolls)
play_dice_game() # Play the game