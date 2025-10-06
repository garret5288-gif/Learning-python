def menu():
    print("\n=== Diary Menu ===\n")
    print("1. Add Entry\n")
    print("2. View Entries\n")
    print("3. Clear Entries\n")
    print("4. Exit\n")

def add_entry():
    with open("diary.txt", "a") as file:
        entry = input("\nWrite your diary entry:\n")
        file.write(entry + "\n")
    print("Entry added.\n")

def view_entries():
    try:
        with open("diary.txt", "r") as file:
            entries = file.readlines()
            if not entries:
                print("No entries found.\n")
                return
            for i, entry in enumerate(entries, 1):
                print(f"\n{i}. {entry.strip()}")
            print()
                
    except FileNotFoundError:
        print("\nNo entries found.\n")

def clear_entries():
    with open("diary.txt", "w") as file:
        pass  # Just open and close to clear the file
    print("All entries cleared.\n")

def main():
    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            clear_entries()
        elif choice == "4":
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()