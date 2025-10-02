import math

def operation_choice():
    choice = input("Enter choice(1-15): ")
    if choice == 1:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print(f"{a} + {b} = {math.fsum([a, b])}")

def main():
    print("Scientific Calculator")
    print()
    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power")
    print("6. Square Root")
    print("7. Sine")
    print("8. Cosine")
    print("9. Tangent")
    print("10. Absolute Value")
    print("11. Pi")
    print("12. Euler's Number")
    print("13. Logarithm")
    print("14. Factorial")
    print("15. Exit")