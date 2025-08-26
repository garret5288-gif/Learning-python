
# Prompt the user to enter two numbers and choose an arithmetic operation.
num1 = float(input("Enter first number: "))  # Convert input to float
num2 = float(input("Enter second number: "))  # Convert input to float

operation = input("Choose operation (+, -, *, /): ")    

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