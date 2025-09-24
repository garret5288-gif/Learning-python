# A program that allows users to input a list of numbers and perform various operations on that list.
# The user can choose to double the numbers, square them, find even or odd numbers, and remove duplicates.

def get_list(): # get a list of numbers from user
    numbers = [] # Initialize empty list
    while True: # Loop to collect numbers
        user_input = input("Enter number 'type done to finish': ")
        if user_input.lower() == 'done' or user_input == '': # Check for completion
            break
        try:
            number = float(user_input) # Convert input to float
            numbers.append(number) # Add number to list
        except ValueError: # Handle invalid input
            print("Invalid input. Please enter a valid number.")
    return numbers # Return the list of numbers

def double_list(numbers):
    return [x * 2 for x in numbers]

def square_list(numbers):
    return [x ** 2 for x in numbers]

def find_even_numbers(numbers):
    return [x for x in numbers if x % 2 == 0]

def find_odd_numbers(numbers):
    return [x for x in numbers if x % 2 != 0]

def remove_duplicates(numbers):
    return list(set(numbers))

def menu(): # display menu options   
    print("1. Get List")
    print("2. Double List")
    print("3. Square List")
    print("4. Find Even Numbers")
    print("5. Find Odd Numbers")
    print("6. Remove Duplicates")
    print("7. Exit")
        
def main(): # main function to run the program
    numbers = []
    menu() # display menu initially    
    while True:
        choice = input("Enter your choice: ")
        if choice == '1':
            numbers = get_list()
            menu() # display menu again after getting list
        elif choice == '7': # exit option
            print("Exiting the program.")
            break
        else:
            if not numbers: # Ensure list is not empty for other operations
                print("Please get the list first (option 1) before using this feature.")
                continue # Skip to next iteration
            if choice == '2':
                doubled = double_list(numbers)
                print("Doubled List:", doubled)
                menu() # display menu again
            elif choice == '3':
                squared = square_list(numbers)
                print("Squared List:", squared)
                menu()
            elif choice == '4':
                evens = find_even_numbers(numbers)
                print("Even Numbers:", evens)
                menu()
            elif choice == '5':
                odds = find_odd_numbers(numbers)
                print("Odd Numbers:", odds)
                menu()
            elif choice == '6':
                unique = remove_duplicates(numbers)
                print("List without Duplicates:", unique)
                menu()
            else: # invalid choice
                print("Invalid choice. Please select a valid option.")

main()
