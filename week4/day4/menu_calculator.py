# A simple calculator with a menu interface
def menu_calculator(): # Function to display the calculator menu
    print()
    print("Calculator Menu")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")
    print()

def get_float(prompt): # Function to get a valid float input from the user
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

while True: # Main loop to run the calculator
    menu_calculator()
    choice = input("Choose an operation (1-5): ")
    if choice == "1":
        num1 = get_float("Enter first number: ") # Replace num1 = float(input(...)) with num1 = get_float(...)
        num2 = get_float("Enter the second number: ")
        print(f"The result is: {num1 + num2}")
    elif choice == "2":
        num1 = get_float("Enter first number: ")
        num2 = get_float("Enter the second number: ")
        print(f"The result is: {num1 - num2}")
    elif choice == "3":
        num1 = get_float("Enter first number: ")
        num2 = get_float("Enter the second number: ")
        print(f"The result is: {num1 * num2}")
    elif choice == "4":
        num1 = get_float("Enter first number: ")
        num2 = get_float("Enter the second number: ")
        if num2 != 0:
            print(f"The result is: {num1 / num2}")
        else: # Handle division by zero error
            print("Error: Division by zero is not allowed.")
    elif choice == "5": # Exit the calculator
        print("Exiting. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid operation.")
    print()  # Print a new line for better readability