import random

def get_random_number(num1, num2):
    return random.randint(min(num1, num2), max(num1, num2))

while True:
    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        break
    except ValueError:
        print("Please enter valid integers.")

random_num = get_random_number(num1, num2)
print(f"Random number between {num1} and {num2}: {random_num}")