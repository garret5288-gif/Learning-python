# True/False Functions Module
def is_odd(number):
    return number % 2 != 0

def is_even(number):
    return number % 2 == 0

def positive(number):
    return number > 0

def negative(number):
    return number < 0

def is_zero(number):
    return number == 0


def main(): # Test the functions
    print(f"Is odd: {is_odd(number)}")
    print(f"Is even: {is_even(number)}")
    print(f"Is positive: {positive(number)}")
    print(f"Is negative: {negative(number)}")
    print(f"Is zero: {is_zero(number)}")

number = float(input("Enter a number: ")) # Prompt user for a number
main() # Call main function to display results