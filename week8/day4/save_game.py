import json
import random

def rock_paper_scissors(state: dict): # Looping RPS game with scoring
    choices = ['rock', 'paper', 'scissors']
    while True: # game loop
        user = input("Enter rock, paper, or scissors (or 'q' to quit): ").strip().lower()
        if user in ('q', 'quit', 'exit'):
            print("Leaving game...\n")
            break # exit game loop
        if user not in choices: # validate input
            print("Invalid choice. Try again.\n")
            continue
        comp = random.choice(choices)
        print(f"Computer chose: {comp}")
        if user == comp: # tie
            state['ties'] += 1
            state['games'] += 1
            print("It's a tie!\n")
        elif (user == 'rock' and comp == 'scissors') or \
             (user == 'paper' and comp == 'rock') or \
             (user == 'scissors' and comp == 'paper'):
            state['wins'] += 1
            state['games'] += 1
            state['score'] += 1
            print("You win!\n") # user wins
        else: # user loses
            state['losses'] += 1
            state['games'] += 1
            state['score'] -= 1
            print("You lose!\n")
        # Show running score after each round
        show_score(state)

def show_score(state: dict): # Display current score
    print("\n=== Score ===")
    print(f"Games:  {state['games']}")
    print(f"Wins:   {state['wins']}")
    print(f"Losses: {state['losses']}")
    print(f"Ties:   {state['ties']}")
    print(f"Score:  {state['score']}\n")

def save_game(data: dict): # Save game state to file
    try: # save to JSON file
        with open("savegame.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Game saved.\n")
    except OSError as e: # handle file errors
        print(f"Error saving game: {e}\n")

def default_state() -> dict: # Default game state
    return {"games": 0, "wins": 0, "losses": 0, "ties": 0, "score": 0}


def load_game() -> dict: # Load game state from file
    try: # load from JSON file
        with open("savegame.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        base = default_state()
        if isinstance(data, dict): # validate expected keys; if missing, merge with defaults
            for k in base.keys():
                if k in data: # only copy known keys
                    try: # ensure values are integers
                        base[k] = int(data[k])
                    except (ValueError, TypeError):
                        # Ignore bad values; keep default
                        pass
        else:
            print("Save file format unexpected; starting new game.\n")
            return default_state()
        print("Game loaded.\n")
        return base # return loaded data
    except FileNotFoundError:
        print("No saved game found. Starting new game.\n")
        return default_state() # return default state
    except json.JSONDecodeError: # handle JSON errors
        print("Error reading save file. Starting new game.\n")
        return default_state()
    
def main(): # Main program loop
    game_data = default_state()
    while True:
        print("\n=== Game Menu ===\n")
        print("1. Play Rock-Paper-Scissors")
        print("2. Show Score")
        print("3. Save Game")
        print("4. Load Game")
        print("5. Exit\n")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            rock_paper_scissors(game_data)
        elif choice == "2":
            show_score(game_data)
        elif choice == "3":
            save_game(game_data)
        elif choice == "4":
            game_data = load_game()
        elif choice == "5":
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()