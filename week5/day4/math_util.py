# math functions with default parameters and type hints
import math

def add(*args) -> float | int:
    '''Returns the sum of the arguments.

    example: add(3, 6, 3) = 12
    returns: int or float
    '''
    return sum(args)


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
def logarithm(a=1, base=10) -> float | int | str:
    '''Returns the logarithm of a with the given base. Defaults to log(1, 10).
    
    If only a is provided, returns log(a, 10).
    If neither is provided, returns log(1, 10).

    example: logarithm(100, 10) = 2.0
    returns: int, float, or str (error message)
    '''
    if a > 0 and base > 1:
        return math.log(a, base)
    else:
        return "Invalid input for logarithm"    

def factorial(n=0) -> int | str:
    '''Returns the factorial of n. Defaults to 0!.
    
    If only n is provided, returns n!.
    If nothing is provided, returns 0!.

    example: factorial(5) = 120
    returns: int or str (error message)
    '''
    if n >= 0:
        return math.factorial(n)
    else:
        return "Invalid input for factorial"

def sine(angle_rad=0) -> float:
    '''Returns the sine of the given angle in radians. Defaults to sin(0).
    
    If angle_rad is provided, returns sin(angle_rad).
    If nothing is provided, returns sin(0).

    example: sine(math.pi/2) = 1.0
    returns: float
    '''
    return math.sin(angle_rad)

def cosine(angle_rad=0) -> float:
    '''Returns the cosine of the given angle in radians. Defaults to cos(0).
    
    If angle_rad is provided, returns cos(angle_rad).
    If nothing is provided, returns cos(0).

    example: cosine(math.pi) = -1.0
    returns: float
    '''
    return math.cos(angle_rad)

def tangent(angle_rad=0) -> float | str:
    '''Returns the tangent of the given angle in radians. Defaults to tan(0).
    
    If angle_rad is provided, returns tan(angle_rad).
    If nothing is provided, returns tan(0). Returns error if undefined.

    example: tangent(math.pi/4) = 1.0
    returns: float or str (error message)
    '''
    try:
        return math.tan(angle_rad)
    except ValueError:
        return "Tangent undefined for this angle"
    finally:
        pass
 
def absolute(value=0) -> float | int:
    '''Returns the absolute value of the given number. Defaults to |0|.
    
    If value is provided, returns |value|.
    If nothing is provided, returns |0|.

    example: absolute(-10) = 10
    returns: int or float
    '''
    return abs(value)

def pi() -> float:
    '''Returns the value of π (pi).
    
    example: pi() = 3.141592653589793
    returns: float
    '''
    return math.pi

def e() -> float:
    '''Returns the value of e (Euler's number).
    
    example: e() = 2.718281828459045
    returns: float
    '''
    return math.e

add(4, 5, 6)  # Example usage of the modified add function

if __name__ == "__main__":
    # simple tests
    print("Addition:", add(3, 5))           # 8
    print("Subtraction:", subtract(10, 4))   # 6
    print("Multiplication:", multiply(7, 6)) # 42
    print("Division:", divide(20, 4))        # 5.0
    print("Power:", power(3, 3))             # 27
    print("Square Root:", square_root(16))   # 4.0
    print("Logarithm:", logarithm(100, 10)) # 2.0
    print("Factorial:", factorial(5))        # 120
    print("Sine (π/2):", sine(math.pi/2))   # 1.0
    print("Cosine (π):", cosine(math.pi))   # -1.0
    print("Tangent (π/4):", tangent(math.pi/4)) # 1.0
    print("Absolute:", absolute(-15))        # 15
    print("Value of π:", pi())               # 3.141592653589793
    print("Value of e:", e())                 # 2.718281828459045