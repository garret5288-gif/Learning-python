import datetime # Import datetime module for timestamps

now = datetime.datetime.now() # Get current date and time

def menu(): # Display menu options
    print("\n=== Log Menu ===\n")
    print("1. Add Log Entry\n")
    print("2. View Log Entries\n")
    print("3. Clear Log Entries\n")
    print("4. Exit\n")

def add_log_entry(): # Add a new log entry
    with open("log_file.txt", "a") as file: # open file for appending
        entry = input("\nWrite your log entry:\n")
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S") # format timestamp
        file.write(f"[{timestamp}] {entry}\n")
    print("Log entry added.\n")

def view_log_entries(): # View all log entries
    try:
        with open("log_file.txt", "r") as file: # open file for reading
            entries = file.readlines()
            if not entries:
                print("No log entries found.\n")
                return
            for i, entry in enumerate(entries, 1): # display entries with numbering
                print(f"\n{i}. {entry.strip()}")
            print()

    except FileNotFoundError: # file does not exist
        print("\nNo log entries found.\n")

def clear_log_entries(): # Clear all log entries
    with open("log_file.txt", "w") as file:
        pass  # Just open and close to clear the file
    print("All log entries cleared.\n")

def main(): # Main program loop
    while True: # Loop until user chooses to exit
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_log_entry()
        elif choice == "2":
            view_log_entries()
        elif choice == "3":
            clear_log_entries()
        elif choice == "4":
            print("Exiting...\n")
            break
        else: # Handle invalid menu choices
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()