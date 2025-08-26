# simple calculator that performs basic arithmetic operations
operation = input("Enter operation (+, -, *, /): ")
num1 = float(input('Enter the first number: '))
num2 = float(input('Enter the second number: '))
# used the round function to limit the result to 2 decimal places
if operation == '+':
    result = num1 + num2
elif operation == '-':
    result = num1 - num2
elif operation == '*':
    result = num1 * num2    
elif operation == '/':
    if num2 != 0:
        result = num1 / num2        
    else:
        result = "Error: Division by zero is not allowed."
else:
    result = "Invalid operation. Please enter one of +, -, *, /."

print("The result is", result)