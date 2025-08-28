def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")

def get_operation(prompt):
    valid_ops = {"+", "-", "*", "/"}
    while True:
        op = input(prompt)
        if op in valid_ops:
            return op
        else:
            print("Invalid operation. Please choose one of +, -, *, /.")

num1 = get_float("Enter first number: ")
num2 = get_float("Enter second number: ")
operation = get_operation("Choose operation (+, -, *, /): ")

if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    if num2 != 0:  # Check for division by zero
        result = num1 / num2
    else:
        result = "Error: Division by zero"  # Handle division by zero error
else:
    result = "Invalid operation"  # Handle invalid operation input

print("Result:", result)