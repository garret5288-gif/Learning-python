# Word counter program

def word_counter(text):
    word_freq = {}  # Dictionary to store word frequencies
    words = text.split()  # Split text into words
    for word in words:
        word = word.lower().strip('.,!?;"\'()[]{}')  # Normalize words
        if word:  # Ensure word is not empty
            word_freq[word] = word_freq.get(word, 0) + 1  # Count frequency
    return word_freq

def main(): # Main function to run the word counter
    print("Word Counter Program")
    text = input("Enter your text: ") # Get user input
    frequencies = word_counter(text) # Get word frequencies
    print("Word Frequencies:") # Display the frequencies
    for word, count in frequencies.items(): # Loop through the dictionary
        print(f"{word}: {count}")

main()