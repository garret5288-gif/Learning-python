# Function to get valid user input
def get_valid_input(prompt, format_func):
    while True: # Loop until valid input is received
        value = input(prompt).strip()
        if value:
            return format_func(value)
        else: # Check if input is not empty
            print("Input cannot be empty. Please try again.")

user_name = get_valid_input("Enter your username: ", str.lower)
city = get_valid_input("Enter your city: ", str.capitalize)
school = get_valid_input("Enter the school you graduated from: ", str.title)
print(f"Hello, {user_name} from {city}, graduate of {school}!")# Print everything with proper formatting
