# Magic 8 ball game practice

import random
# imported random module for generating random responses
question = input("Ask a yes/no question or quit to quit: ")
responses = [
    "yes",
    "no",
    "maybe",
    "ask again later"
]
response = random.choice(responses)
quit = False
while not quit:
    question = input("Ask a yes/no question or quit to quit: ") #changed answer_1 to question for clarity
    if question.strip().lower() == "quit": # Used strip() and lower() to handle whitespace and case
        quit = True
    else:
        response = random.choice(responses)
        print(f"Question: {question}\nAnswer: {response}")