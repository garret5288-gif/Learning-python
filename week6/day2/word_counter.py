# Word Frequency Counter

paragraph = "When I was a child, I used to think that the world was flat. " \
"I believed that if I traveled far enough, I would reach the edge of the world. "

def word_frequency(text):# Count frequency of each word
    words = text.split() # Split text into words
    unique_words = [] # List to hold unique words
    frequency = [] # List to hold word frequencies
    for word in words: # Iterate through words
        if word not in unique_words: # Check if word is unique
            unique_words.append(word) # Add to unique words
            frequency.append(words.count(word)) # Count occurrences
    for i in range(len(unique_words)): # Print each word with its frequency
        print(f"{unique_words[i]}: {frequency[i]}") 

word_frequency(paragraph)