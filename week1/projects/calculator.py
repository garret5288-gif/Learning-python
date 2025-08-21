# simple calculator that performs basic arithmetic operations

operation = input("Enter operation (+, -, *, /): ")
num1 = float(input('Enter the first number: '))
num2 = float(input('Enter the second number: '))

if operation == '+':
    result = num1 + num2
    print(f"The result of {num1} + {num2} is {round(result, 2)}") 
elif operation == '-':
    result = num1 - num2
    print(f"The result of {num1} - {num2} is {round(result, 2)}") 
elif operation == '*':
    result = num1 * num2
    print(f"The result of {num1} * {num2} is {round(result, 2)}")
elif operation == '/':
    if num2 != 0:
        result = num1 / num2
        print(f"The result of {num1} / {num2} is {round(result, 2)}")
    else:
        print("Error: Division by zero is not allowed.")
else: 
    print("Invalid operation. Please enter one of +, -, *, /.")