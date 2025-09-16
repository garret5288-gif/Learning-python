# Making 5 defined functions

def happy_birthday(name, age): # Function to wish happy birthday
    while True: # Input validation loop for name
        name = name.strip().title() # Standardize name format
        if name == "" or not name.replace(" ", "").isalpha():
            print("Please enter a valid name.") # Check for empty or non-alphabetic names
            name = input("Enter your name: ").strip()
            continue
        break

    while True: # Input validation loop for age
        age = age.strip()
        if not age.isdigit() or int(age) < 0: # Check for non-numeric or negative ages
            print("Please enter a valid age.")
            age = input("Enter your age: ").strip()
        else:
            break

    print(f"Happy Birthday {name}!")
    print(f"You are {age} years old!")

def over_21(age): # Function to check if user is over 21
    if int(age) >= 21:
        print("You are at least 21.")
    else:
        print("You are under 21.")

def get_drink(age): # Function to suggest drink based on age
    if int(age) >= 21:
        return "You can have a cocktail."
    else:
        return "You can have a soda."

def main(): # Main function to run the program
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    happy_birthday(name, age)
    over_21(age)
    print(get_drink(age))
    how_long_to_21(age)

def how_long_to_21(age): # Function to calculate years until 21
    if int(age) < 21:
        years_left = 21 - int(age)
        print(f"You have {years_left} years until you are 21.")
    else:
        print()

main() # Call main function to execute the program
