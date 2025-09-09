# Input Validator
user_name = input("Enter your username: (must be at least 6 characters long and contain one number) ").strip()
while True: # Loop until valid input is received
    if user_name == "": # Check for empty input
        print("Username cannot be empty.")
    elif len(user_name) < 6: # Check for minimum length
        print("Username must be at least 6 characters long.")
    elif not any(char.isdigit() for char in user_name): # Check for at least one number
        print("Username must contain at least one number.")
    else:
        print("Valid username.")
        break
    user_name = input("Enter your username: (must be at least 6 characters long and contain one number) ").strip()