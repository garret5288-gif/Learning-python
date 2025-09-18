def is_number(number):
    '''
    Checks if the provided input is a number (int or float).

    Example: is_number(10) = True
    Example: is_number(10.5) = True
    Example: is_number("10") = False
    returns: bool
    '''
    return isinstance(number, (int, float))

def is_nonempty(value):
    '''
    Checks if the provided value is a non-empty string.

    Example: is_nonempty("Hello") = True
    Example: is_nonempty("") = False
    Example: is_nonempty("   ") = False
    returns: bool
    '''
    return isinstance(value, str) and len(value.strip()) > 0

def is_letters(text):
    '''
    Checks if the provided text contains only letters (a-z, A-Z).

    Example: is_letters("Hello") = True
    Example: is_letters("Hello123") = False
    returns: bool
    '''
    return text.isalpha()

def is_alphanumeric(text):
    '''
    Checks if the provided text contains only alphanumeric characters (letters and numbers).

    Example: is_alphanumeric("Hello123") = True
    Example: is_alphanumeric("Hello 123") = False
    returns: bool
    '''
    return text.isalnum()

if __name__ == "__main__":
    # Test cases for validation functions
    print(is_number(10))          # True
    print(is_number(10.5))        # True
    print(is_number("10"))        # False

    print(is_nonempty("Hello"))   # True
    print(is_nonempty("   "))     # False
    print(is_nonempty(""))         # False

    print(is_letters("Hello"))    # True
    print(is_letters("Hello123")) # False

    print(is_alphanumeric("Hello123")) # True
    print(is_alphanumeric("Hello 123"))# False
