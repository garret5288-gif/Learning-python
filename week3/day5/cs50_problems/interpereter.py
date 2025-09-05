# math interpreter
expression = input("Enter an expression: ").strip() # e.g., "3 + 4"
elements = expression.split() # Split the input into components
num1 = int(elements[0]) # Convert the first element to an integer
num2 = int(elements[2]) # Convert the second element to an integer
operator = elements[1] # Get the operator

if operator == "+":
    result = num1 + num2
elif operator == "-":
    result = num1 - num2
elif operator == "*":
    result = num1 * num2
elif operator == "/":
    result = num1 / num2
else:
    print("Unknown operator")

print(f"{result:.1f}") # Print the result formatted to one decimal place