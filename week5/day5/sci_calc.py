from math_utilities import (
    add, subtract, multiply, divide, power, square_root, logarithm,
    factorial, absolute, sine, cosine, tangent
)
import math

# imported math_utilities functions
# Main function to run the scientific calculator
def main(): # main function to run the program
    while True: # main loop with options
        print("\nScientific Calculator Menu")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Power")
        print("6. Square Root")
        print("7. Logarithm")
        print("8. Factorial")
        print("9. Absolute Value")
        print("10. Sine (radians)")
        print("11. Cosine (radians)")
        print("12. Tangent (radians)")
        print("0. Exit")
        choice = input("Choose an operation (0-12): ")

        try: # handle user choice
            if choice == "0":
                print("Goodbye!")
                break # exit the loop and program
            elif choice == "1":
                a = float(input("First number: "))
                b = float(input("Second number: "))
                print("Result:", add(a, b)) # addition
            elif choice == "2":
                a = float(input("First number: "))
                b = float(input("Second number: "))
                print("Result:", subtract(a, b)) # subtraction
            elif choice == "3":
                a = float(input("First number: "))
                b = float(input("Second number: "))
                print("Result:", multiply(a, b)) # multiplication
            elif choice == "4":
                a = float(input("Numerator: "))
                b = float(input("Denominator: "))
                print("Result:", divide(a, b)) # division
            elif choice == "5":
                a = float(input("Base: "))
                b = float(input("Exponent: "))
                print("Result:", power(a, b)) # power
            elif choice == "6":
                a = float(input("Number: "))
                print("Result:", square_root(a)) # square root
            elif choice == "7":
                a = float(input("Number: "))
                base = float(input("Base (default e, press Enter for e): ") or math.e)
                print("Result:", logarithm(a, base)) # logarithm
            elif choice == "8":
                n = int(input("Integer: "))
                print("Result:", factorial(n)) # factorial
            elif choice == "9":
                a = float(input("Number: "))
                print("Result:", absolute(a)) # absolute value
            elif choice == "10":
                angle = float(input("Angle in radians: "))
                print("Result:", sine(angle)) # sine
            elif choice == "11":
                angle = float(input("Angle in radians: "))
                print("Result:", cosine(angle)) # cosine
            elif choice == "12":
                angle = float(input("Angle in radians: "))
                print("Result:", tangent(angle)) # tangent
            else:
                print("Invalid choice.") # invalid choice
        except Exception as e: # catch all exceptions
            print("Error:", e)

if __name__ == "__main__":
    main() # run the main function