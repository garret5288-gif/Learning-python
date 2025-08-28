# Check for valid username
user_name = input("Enter your username that doesn't contain numbers: ").capitalize()

while not user_name.isalpha():# Check if the username contains only letters
    print("Invalid username. Please use only letters.")

age = input("Enter your age: ")

while not age.isdigit():# Check if the age is a number
    print("Invalid age. Please enter a number.")
print(f"Hello, {user_name} your age is {age}!")

