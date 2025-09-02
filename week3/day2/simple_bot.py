# Simple Yes/No Bot
print("Hello! Ask me some yes or no questions!")

import random # Importing random module to generate random responses

while True: # Main loop
    question = input("Your question, or type 'exit' to quit: ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    elif question.strip(): # Check if the question is not empty
        answer = random.choice(["Yes", "No",])
        print(f"Bot: {answer}") 
    else:
        print("Bot: Please ask yes or no questions!")