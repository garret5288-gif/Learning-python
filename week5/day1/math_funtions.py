# Math functions module

def add(a, b):  # Adds two numbers
    return a + b

def subtract(a, b):  # Subtracts second number from first
    return a - b

def multiply(a, b):  # Multiplies two numbers
    return a * b

def divide(a, b):  # Divides first number by second
    if b != 0:
        return a / b
    else:
        return "Division by zero error"

def get_integer(prompt):  # Prompts user for two integers
    while True:  # Loop until valid input is received
        try:  # Try to convert input to integers
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
            return a, b
        except ValueError:  # Handle non-integer input
            print("Invalid input. Please enter an integer.")

print ("Give two numbers to add")
a, b = get_integer(add)
print(f"{a} + {b} = {add(a, b)}") # Display result of addition

print ("Give two numbers to subtract")
a, b = get_integer(subtract)
print(f"{a} - {b} = {subtract(a, b)}")

print ("Give two numbers to multiply")
a, b = get_integer(multiply)
print(f"{a} * {b} = {multiply(a, b)}")

print ("Give two numbers to divide")
a, b = get_integer(divide)
print(f"{a} / {b} = {divide(a, b)}")
