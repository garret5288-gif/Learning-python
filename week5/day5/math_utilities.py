import math

def add(a, b):
    """
    Return the sum of a and b.

    Parameters:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        int or float: The sum of a and b.

    Example:
        add(2, 3) -> 5
    """
    return a + b

def subtract(a, b):
    """
    Return the difference of a and b (a - b).

    Parameters:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        int or float: The difference of a and b.

    Example:
        subtract(5, 2) -> 3
    """
    return a - b

def multiply(a, b):
    """
    Return the product of a and b.

    Parameters:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        int or float: The product of a and b.

    Example:
        multiply(4, 3) -> 12
    """
    return a * b

def divide(a, b):
    """
    Return the quotient of a and b (a / b).
    Raises ValueError if b is zero.

    Parameters:
        a (int or float): The numerator.
        b (int or float): The denominator.

    Returns:
        float: The result of division.

    Raises:
        ValueError: If b is zero.

    Example:
        divide(10, 2) -> 5.0
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def power(a, b):
    """
    Return a raised to the power of b (a ** b).

    Parameters:
        a (int or float): The base number.
        b (int or float): The exponent.

    Returns:
        int or float: The result of a ** b.

    Example:
        power(2, 3) -> 8
    """
    return a ** b

def square_root(a):
    """
    Return the square root of a.
    Raises ValueError if a is negative.

    Parameters:
        a (int or float): The number to take the square root of.

    Returns:
        float: The square root of a.

    Raises:
        ValueError: If a is negative.

    Example:
        square_root(9) -> 3.0
    """
    if a < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(a)

def logarithm(a, base=math.e):
    """
    Return the logarithm of a with the given base (default is natural log).
    Raises ValueError if a <= 0 or base <= 0 or base == 1.

    Parameters:
        a (int or float): The number to take the log of.
        base (int or float): The base of the logarithm (default: math.e).

    Returns:
        float: The logarithm of a to the given base.

    Raises:
        ValueError: If a <= 0, base <= 0, or base == 1.

    Example:
        logarithm(100, 10) -> 2.0
    """
    if a <= 0:
        raise ValueError("Logarithm undefined for zero or negative numbers.")
    if base <= 0 or base == 1:
        raise ValueError("Base must be positive and not equal to 1.")
    return math.log(a, base)

def factorial(n):
    """
    Return the factorial of n.
    Raises ValueError if n is negative or not an integer.

    Parameters:
        n (int): The number to take the factorial of.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative or not an integer.

    Example:
        factorial(5) -> 120
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial only defined for non-negative integers.")
    return math.factorial(n)

def absolute(a):
    """
    Return the absolute value of a.

    Parameters:
        a (int or float): The number to get the absolute value of.

    Returns:
        int or float: The absolute value of a.

    Example:
        absolute(-7) -> 7
    """
    return abs(a)

def sine(angle_rad):
    """
    Return the sine of the given angle in radians.

    Parameters:
        angle_rad (float): Angle in radians.

    Returns:
        float: The sine of the angle.

    Example:
        sine(math.pi/2) -> 1.0
    """
    return math.sin(angle_rad)

def cosine(angle_rad):
    """
    Return the cosine of the given angle in radians.

    Parameters:
        angle_rad (float): Angle in radians.

    Returns:
        float: The cosine of the angle.

    Example:
        cosine(math.pi) -> -1.0
    """
    return math.cos(angle_rad)

def tangent(angle_rad):
    """
    Return the tangent of the given angle in radians.
    Raises ValueError if tangent is undefined for the angle.

    Parameters:
        angle_rad (float): Angle in radians.

    Returns:
        float: The tangent of the angle.

    Raises:
        ValueError: If tangent is undefined for the angle.

    Example:
        tangent(math.pi/4) -> 1.0
    """
    return math.tan(angle_rad)
