# A simple math games program with addition, subtraction, and multiplication quizzes.
# The user can choose a game, answer 10 questions, and receive a score at the end.
import random # Import random module for generating random numbers
import json # Import json module for saving/loading settings

SETTINGS_FILE = "math_settings.json" # File to save settings

def default_settings(): # Default settings
    return {
        "num_questions": 10,
        "min_num": 1,
        "max_num": 12,
    }

def save_settings(settings: dict): # Save settings to file
    try: # Save settings to JSON file
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print("Settings saved.\n")
    except OSError as e: # handle file errors
        print(f"Failed to save settings: {e}\n")

def load_settings() -> dict: # Load settings from file
    try: # Load settings from JSON file
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        base = default_settings()
        if isinstance(data, dict): # validate expected keys; if missing, merge with defaults
            for k in base:
                if k in data:
                    try:
                        base[k] = int(data[k])
                    except (ValueError, TypeError): # Ignore bad values; keep default
                        pass
        print("Settings loaded.\n")
        return base
    except FileNotFoundError: # file does not exist
        print("No saved settings found. Using defaults.\n")
        return default_settings()
    except json.JSONDecodeError: # handle JSON errors
        print("Settings file invalid. Using defaults.\n")
        return default_settings()

def prompt_int(label: str, default: int) -> int: # Prompt for integer with default
    raw = input(f"{label} [{default}]: ").strip()
    if raw == "": # Use default if input is empty
        return default
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid number; keeping previous value.")
        return default

def show_settings(settings: dict): # Display current settings
    print("\nCurrent Settings:")
    print(f" - Questions per quiz: {settings['num_questions']}")
    print(f" - Min number:         {settings['min_num']}")
    print(f" - Max number:         {settings['max_num']}\n")

def edit_settings(settings: dict): # Edit settings interactively
    show_settings(settings) # show current settings
    num_q = prompt_int("Questions per quiz", settings["num_questions"])
    min_n = prompt_int("Min number", settings["min_num"])
    max_n = prompt_int("Max number", settings["max_num"])
    # validations
    if num_q < 1: # validate num_questions
        print("Questions must be at least 1. Setting to 1.")
        num_q = 1
    if min_n > max_n: # validate min/max
        print("Min was greater than Max; swapping them.")
        min_n, max_n = max_n, min_n
    settings.update({ # update settings
        "num_questions": num_q,
        "min_num": min_n,
        "max_num": max_n,
    })
    show_settings(settings)

def settings_menu(settings: dict): # Settings menu loop
    while True:
        print("Settings Menu")
        print("1. View Settings")
        print("2. Edit Settings")
        print("3. Save Settings")
        print("4. Load Settings")
        print("5. Back")
        ch = input("Choose (1-5): ").strip()
        if ch == "1":
            show_settings(settings)
        elif ch == "2":
            edit_settings(settings)
        elif ch == "3":
            save_settings(settings)
        elif ch == "4":
            loaded = load_settings()
            settings.clear()
            settings.update(loaded)
        elif ch == "5":
            print()
            break
        else:
            print("Invalid choice.\n")

def main(): # Define main function
    settings = default_settings()
    while True: # Main loop to display menu and handle user choice
        print("Welcome to Math Games!")
        print("1. Addition Quiz")
        print("2. Subtraction Quiz")
        print("3. Multiplication Quiz")
        print("4. Settings")
        print("5. Exit")

        choice = input("Choose a game (1-5): ") # Prompt user for game choice
        if choice == '1':
            quiz("addition", settings)
        elif choice == '2':
            quiz("subtraction", settings)
        elif choice == '3':
            quiz("multiplication", settings)
        elif choice == '4':
            settings_menu(settings)
        elif choice == '5': # Exit option
            print("Thanks for playing!")
            break
        else: # Handle invalid input
            print("Invalid choice. Please select a number between 1 and 4.")

def quiz(operation, settings): # Define quiz function (uses settings)
    score = 0
    num_q = settings.get("num_questions", 10)
    lo = settings.get("min_num", 1)
    hi = settings.get("max_num", 12)
    # Safety checks
    if lo > hi:
        lo, hi = hi, lo
    if num_q < 1:
        num_q = 10
    for i in range(num_q): # Ask N questions
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
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
            # Optionally avoid negatives by ensuring a >= b
            if a < b:
                a, b = b, a
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
    print(f"Your score: {score}/{num_q}") # Display user's score
    print()
   
main() # Call main function to start the program
