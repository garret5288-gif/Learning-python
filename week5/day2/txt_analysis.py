# Text Analysis Module
def text_analysis(text):
    word_count = len(text.split()) # Count words by splitting text
    char_count = len(text) # Count characters in text
    return word_count, char_count

text = input("Enter some text: ")
words, chars = text_analysis(text)
print(f"Word count: {words}") # Count words
print(f"Character count: {chars}") # Count characters