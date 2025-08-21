
import random

answer_1 = input("Ask a yes/no question or quit to quit: ")
responses = [
    "yes",
    "no",
    "maybe",
    "ask again later"
]
response = random.choice(responses)
quit = False
while not quit:
    answer_1 = input("Ask a yes/no question or quit to quit: ")
    if answer_1.lower() == "quit":
        quit = True
    else:
        response = random.choice(responses)
        print(f"Question: {answer_1}\nAnswer: {response}")