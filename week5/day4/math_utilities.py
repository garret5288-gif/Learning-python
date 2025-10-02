
def add(a, b) -> float:
    '''Returns the sum of a and b.'''
    return a + b

def subtract(a, b) -> float:
    '''Returns the difference of a and b.'''
    return a - b

def multiply(a, b) -> float:
    '''Returns the product of a and b.'''
    return a * b

def divide(a, b) -> float | str:
    '''Returns the quotient of a and b.'''
    if b != 0:
        return a / b
    else:
        return "Division by zero error"

def power(a, b) -> float:
    '''Returns a raised to the power of b.'''
    return a ** b

def square_root(a) -> float | str:
    '''Returns the square root of a.'''
    if a >= 0:
        return a ** 0.5
    else:
        return "Square root of negative number error"
    
if __name__ == "__main__":
    # Example usage
    print("Addition:", add(3, 6))
    print("Subtraction:", subtract(9, 3))
    print("Multiplication:", multiply(9, 5))
    print("Division:", divide(10, 0))
    print("Power:", power(4, 3))
    print("Square Root:", square_root(-8))