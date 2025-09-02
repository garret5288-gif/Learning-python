while True:
    number_input = input("Enter a number: ")
    if number_input.lstrip('-').isdigit():  # Allow for negative numbers
        number = int(number_input)
        break
    else:
        print("Invalid input. Please enter a valid number.")

if number % 2 == 0:
    print(f"{number} is even.")
else:
    print(f"{number} is odd.")
