import math
# Scientific Calculator with various functions

def main(): # main function to run the program
    print()
    print("*********************")
    print("Scientific Calculator")
    print("*********************")
    while True: # main loop with options
        print("Select operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Power")
        print("6. Square Root")
        print("7. Sine (degrees)")
        print("8. Cosine (degrees)")
        print("9. Tangent (degrees)")
        print("10. Logarithm")
        print("11. Exponential (e^x)")
        print("12. Factorial")
        print("13. Absolute Value")
        print("14. Degrees to Radians")
        print("15. Radians to Degrees")
        print("0. Exit") # exit option
        choice = input("Enter choice (0-15): ") # get user choice
        print()
        if choice == '0': # exit
            print("Exiting calculator.")
            break # breaks the loop and exits
        elif choice in {'1','2','3','4','5'}: # operations needing two numbers
            while True: # loop to get two valid numbers from user
                try: 
                    a = float(input("Enter first number: "))
                    b = float(input("Enter second number: "))
                    break
                except ValueError: # handle invalid input
                    print("Invalid input. Please enter valid numbers.")
            if choice == '1': # addition
                print("Result:", a + b)
            elif choice == '2': # subtraction
                print("Result:", a - b)
            elif choice == '3': # multiplication
                print("Result:", a * b)
            elif choice == '4': # division
                if b == 0: # handle division by zero
                    print("Error: Division by zero.")
                else:
                    print("Result:", a / b)
            elif choice == '5': # power
                print("Result:", math.pow(a, b))
        elif choice == '6': # square root
            while True: # loop to get valid number from user
                try:
                    a = float(input("Enter number: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            if a < 0: # invalid input
                print("Error: Cannot take square root of negative number.")
            else: # valid input
                print("Result:", math.sqrt(a))
        elif choice == '7': 
            while True:
                try:
                    angle = float(input("Enter angle in degrees: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            radians = math.radians(angle)
            print("Result:", math.sin(radians))
        elif choice == '8':
            while True:
                try:
                    angle = float(input("Enter angle in degrees: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            radians = math.radians(angle)
            print("Result:", math.cos(radians))
        elif choice == '9':
            while True:
                try:
                    angle = float(input("Enter angle in degrees: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            radians = math.radians(angle)
            print("Result:", math.tan(radians))
        elif choice == '10':
            while True:
                try:
                    a = float(input("Enter number to take log of: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            base = input("Enter base (press Enter for natural log): ")
            if a <= 0:
                print("Error: Logarithm undefined for zero or negative numbers.")
            else:
                if base.strip() == "": # natural log
                    print("Result:", math.log(a))
                else:
                    try: # convert base to float
                        base_val = float(base)
                        if base_val <= 0 or base_val == 1:
                            print("Error: Base must be positive and not equal to 1.")
                        else:
                            print("Result:", math.log(a, base_val))
                    except ValueError:
                        print("Invalid base.")
        elif choice == '11':
            while True:
                try:
                    a = float(input("Enter exponent for e^x: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            print("Result:", math.exp(a))
        elif choice == '12':
            while True:
                try:
                    a = float(input("Enter number for factorial: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            if a < 0 or not a.is_integer():
                print("Error: Factorial only defined for non-negative integers.")
            else:
                print("Result:", math.factorial(int(a)))
        elif choice == '13':
            while True:
                try:
                    a = float(input("Enter number for absolute value: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            print("Result:", abs(a))
        elif choice == '14':
            while True:
                try:
                    deg = float(input("Enter degrees: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            print("Radians:", math.radians(deg))
        elif choice == '15':
            while True:
                try:
                    rad = float(input("Enter radians: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            print("Degrees:", math.degrees(rad))
        else: # invalid choice
            print("Invalid choice. Please try again.")

main() # run the calculator