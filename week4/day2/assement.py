# menu program that keeps going until the user chooses to exit.
while True: # Main loop to display the menu and handle user input
    print("********** MENU **********")
    print("1. Help")
    print("2. Settings")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ").strip() # Get user input
    if choice == "": # Check for empty input
        print("Input cannot be empty, please try again.")
    elif not choice.isdigit() or int(choice) not in range(1, 4): # Validate input range
        print("Invalid input, please enter a number between 1 and 3.")
    elif choice == "1":
        print("Help selected. Here is some help information...")
    elif choice == "2":
        print("Settings selected. Here are the settings...")
    elif choice == "3": # Exit option
        print("Exiting the program. Goodbye!")
        break
