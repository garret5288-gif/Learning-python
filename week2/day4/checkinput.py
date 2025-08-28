user_name = input("Enter your username that doesn't contain numbers: ").capitalize()

while not user_name.isalpha():
    print("Invalid username. Please use only letters.")
    user_name = input("Enter your username that doesn't contain numbers: ").capitalize()

age = input("Enter your age: ")

while not age.isdigit():
    print("Invalid age. Please enter a number.")
    age = input("Enter your age: ")
print(f"Hello, {user_name} your age is {age}!")

