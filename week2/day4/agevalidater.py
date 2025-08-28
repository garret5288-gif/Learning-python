# Made age calculation with user input defense
while True: # Loop until valid input is received
    birth_year = input("Enter your birth year (YYYY): ")
    if birth_year.isdigit(): # Check if input is numeric
        birth_year = int(birth_year)
        if birth_year > 2025: # Check if birth year is valid
            print("Birth year cannot be greater than 2025. Please try again.")
        else:
            break # Exit the loop if input is valid
    else:
        print("Please enter numbers only for the birth year.")

current_year = 2025
age = current_year - birth_year

print(f"Your age is {age}.")