# A simple menu program that prompts the user to select an option from a list.
# The program validates the input and responds accordingly.
loop = True # Control variable for the
while loop: # Main loop to display the menu and handle user input
    print("\n*** Simple Menu ***")
    for i in range(1, 4): # Display menu options
        print(f"{i}. Option {i}")
    print("4. Exit")

    user_input = input("Enter your choice (1-4): ").strip()
    if user_input == "": # Check for empty input
        print("Input cannot be empty, please try again.")
    elif not user_input.isdigit() or int(user_input) not in range(1, 5): # Validate input range
        print("Invalid input, please enter a number between 1 and 4.")
    elif user_input == "1":
        print("You selected Option 1")
    elif user_input == "2":
        print("You selected Option 2")
    elif user_input == "3":
        print("You selected Option 3")
    elif user_input == "4":
        print("Exiting the program. Goodbye!")
        loop = False # Exit the loop and end the program
