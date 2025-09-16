# Input_validation.py
# This script validates user input for age and email address.
def is_valid_age(age): # Function to validate age
    if age.isdigit() and 0 <= int(age) <= 120: # Check if age is a digit and within the valid range
        return True
    return False # Function to validate email format
    
def is_valid_email(email): # Simple email validation
    if "@" in email and "." in email.split("@")[-1]: # Check for basic email structure
        return True
    return False

user_age = input("Enter your age: ") # Prompt user for age
while not is_valid_age(user_age): # Validate age input
    print("Invalid age. Please enter a number between 0 and 120.")
    user_age = input("Enter your age: ")

user_email = input("Enter your email address: ")
while not is_valid_email(user_email):
    print("Invalid email format. Please try again.")
    user_email = input("Enter your email address: ")