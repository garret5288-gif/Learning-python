while True:
    if number_input.lstrip('-').isdigit():  # Allow for negative numbers
        number = int(number_input)
        break
    else:
        print("Invalid input. Please enter a valid number.")

if number > 0:
    print(f"{number} is positive.")
elif number < 0:
    print(f"{number} is negative.")
else:
    print("The number is zero.")
