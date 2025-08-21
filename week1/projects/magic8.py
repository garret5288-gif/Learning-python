# Magic 8 ball game practice

import random

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
    question = input("Ask a yes/no question or quit to quit: ") #changed answer_1 to question
    if question.lower() == "quit":
        quit = True
    else:
        response = random.choice(responses)
        print(f"Question: {question}\nAnswer: {response}")