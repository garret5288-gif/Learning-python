# text processing utilities

def word_count(text: str) -> int:
    '''Returns the number of words in a given text.

    example: word_count("Hello world") = 2
    returns: int
    '''
    words = text.split()
    return len(words)

def char_count(text: str) -> int:
    '''Returns the number of characters in a given text.

    example: char_count("Hello") = 5
    returns: int
    '''
    return len(text)

def space_count(text: str) -> int:
    '''Returns the number of spaces in a given text.

    example: space_count("Hello world") = 1
    returns: int
    '''
    return text.count(' ')


def to_uppercase(text: str) -> str:
    '''Converts the text to uppercase.

    example: to_uppercase("Hello") = "HELLO"
    returns: str
    '''
    return text.upper()

def to_lowercase(text: str) -> str:
    '''Converts the text to lowercase.

    example: to_lowercase("Hello") = "hello"
    returns: str
    '''
    return text.lower()

if __name__ == "__main__":
    sample_text = "Hello World! I am here!."
    print("Sample Text:", sample_text)
    print("Word Count:", word_count(sample_text))
    print("Character Count:", char_count(sample_text))
    print("Space Count:", space_count(sample_text))
    print("Uppercase:", to_uppercase(sample_text))
    print("Lowercase:", to_lowercase(sample_text))