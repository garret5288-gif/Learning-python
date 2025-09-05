import random

while True:
    user = input("Ask a yes/no question: ").strip().lower()
    responses = ["Yes", "No", "Maybe", "Ask again later"]
    if user == "":
        print("Please ask a valid question.")
        continue
    print(random.choice(responses))
    again = input("Do you want to ask another question? (y/n): ").strip().lower()
    if not again == 'y':
        break