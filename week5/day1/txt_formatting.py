# txt_formatting.py
# This script prompts the user for their first and last names, formats them,
def get_full_name(): # Function to get and format full name
    first_name = input("Enter your first name: ").capitalize().strip() # Capitalize and strip whitespace
    last_name = input("Enter your last name: ").capitalize().strip()
    if first_name == "" or last_name == "":
        print("Both first and last names are required.")
    elif not first_name.isalpha() or not last_name.isalpha(): # Validate alphabetic input
        print("Names must contain only alphabetic characters.")
        return get_full_name()  # Recursively prompt until valid input
    return f"{first_name} {last_name}"
print("Full Name:", get_full_name())

get_full_name()
