# calculator functions module

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
