# math functions with default parameters and type hints

def add(a=0, b=0) -> float | int:
    '''Returns the sum of a and b. Defaults to 0.
   
    If only a is provided, returns a + 0.
    If neither is provided, returns 0 + 0.
   
    example: add(3, 6) = 9
    returns: int or float
    '''
    return a + b


def subtract(a=0, b=0) -> float | int:
    '''Returns the difference of a and b. Defaults to 0.
    
    If only a is provided, returns a - 0.
    If neither is provided, returns 0 - 0.

    example: subtract(9, 3) = 6
    returns: int or float
    '''
    return a - b


def multiply(a=1, b=1) -> float | int:
    '''Returns the product of a and b. Defaults to 1.
    
    If only a is provided, returns a * 1.
    If neither is provided, returns 1 * 1.

    example: multiply(9, 5) = 45
    returns: int or float
    '''
    return a * b


def divide(a=1, b=1) -> float | int | str:
    '''Returns the quotient of a and b. Defaults to 1. Returns error if b is 0.
    
    If only a is provided, returns a / 1.
    If neither is provided, returns 1 / 1.

    example: divide(10, 2) = 5.0
    returns: int, float, or str (error message)
    '''
    if b != 0:
        return a / b
    else:
        return "Division by zero error"


def power(a=2, b=2) -> float | int:
    '''Returns a raised to the power of b. Defaults to 2^2.
   
     If only a is provided, returns a ** 2.
    If neither is provided, returns 2 ** 2.

    example: power(4, 3) = 64
    returns: int or float
    '''
    return a ** b


def square_root(a=0) -> float | int | str:
    '''Returns the square root of a. Defaults to 0.
    
    If only a is provided, returns a ** 0.5.
    If nothing is provided, returns 0 ** 0.5.

    example: square_root(9) = 3.0
    returns: int, float, or str (error message)
    '''
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