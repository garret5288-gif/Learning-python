# Simple Diary Application
# Allows users to add, view, and clear diary entries stored in a text file.

def menu(): # Display menu options
    print("\n=== Diary Menu ===\n")
    print("1. Add Entry\n")
    print("2. View Entries\n")
    print("3. Clear Entries\n")
    print("4. Exit\n")

def add_entry(): # Add a new diary entry
    with open("diary.txt", "a") as file: # open file for appending
        entry = input("\nWrite your diary entry:\n")
        file.write(entry + "\n") # write entry to file
    print("Entry added.\n")

def view_entries(): # View all diary entries
    try: # Attempt to read diary entries
        with open("diary.txt", "r") as file: # open file for reading
            entries = file.readlines() # read all lines
            if not entries:
                print("No entries found.\n")
                return
            for i, entry in enumerate(entries, 1): # display entries with numbering
                print(f"\n{i}. {entry.strip()}")
            print()
                
    except FileNotFoundError: # file does not exist
        print("\nNo entries found.\n")

def clear_entries(): # Clear all diary entries
    with open("diary.txt", "w") as file:
        pass  # Just open and close to clear the file
    print("All entries cleared.\n")

def main(): # Main program loop
    while True:  # Loop until user chooses to exit
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
        else:  # Handle invalid menu choices
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()