# Prompt the user for the answer to the Great Question of Life, the Universe and Everything
answer = input("What is the answer to the Great Question of Life, the Universe and Everything? ").strip().lower()
if answer == "42" or answer == "forty two" or answer == "forty-two": # Check for all valid answers
    print("Yes")
else:
    print("No")

