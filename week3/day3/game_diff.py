def menu():
    print("Welcome to the game please choose difficulty level:\n")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

def get_difficulty():
    difficulty = input("Enter the difficulty level (1-3): ").strip()
    while difficulty not in ["1", "2", "3"]:
        print("Invalid input. Please try again.")
        difficulty = input("Enter the difficulty level (1-3): ").strip()
    return difficulty

menu()
difficulty = get_difficulty()

if difficulty == "1":
    print("You have selected Easy difficulty.")
elif difficulty == "2":
    print("You have selected Medium difficulty.")
elif difficulty == "3":
    print("You have selected Hard difficulty.")
else:
    print("Invalid difficulty level.")

