# Function Calculator Module
def calculator(num1, operator, num2):
    # Validate inputs
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        return "Error: Inputs must be numbers"
    elif operator == '+': # Addition
        return num1 + num2
    elif operator == '-': # Subtraction
        return num1 - num2
    elif operator == '*': # Multiplication
        return num1 * num2
    elif operator == '/': # Division
        if num2 != 0:
            return num1 / num2
        return "Error: Division by zero"
    return "Error: Invalid operator"
# Get user inputs
num1 = float(input("Enter first number: ")) 
operator = input("Enter operator (+, -, *, /): ")
num2 = float(input("Enter second number: "))

result = calculator(num1, operator, num2)
print(f"Result: {num1} {operator} {num2} = {result}")