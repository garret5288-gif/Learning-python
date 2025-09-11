# Password validation script
def main(): # Display password criteria
    print("Enter a password that meets the following criteria:")
    print("- At least 8 characters long")
    print("- Contains both uppercase and lowercase characters")
    print("- Includes at least one numeric digit")
    print("- Has at least one special character (e.g., !@#$%^&*)")

def special_characters(): # Define special characters
    return "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"  

main()
while True:
    password = input("Enter your password: ") # Get password input from user
     # Check password criteria
    if len(password) < 8: # Check length
        print("Password must be at least 8 characters long.")
    elif password.lower() == password: # Check for uppercase letter
        print("Password must contain at least one uppercase letter.")
    elif password.upper() == password: # Check for lowercase letter
        print("Password must contain at least one lowercase letter.")
    elif not any(char.isdigit() for char in password): # Check for numeric digit
        print("Password must contain at least one numeric digit.")
    elif not any(char in special_characters() for char in password): # Check for special character
        print("Password must contain at least one special character.")
    else:
        print("Password is valid.")
        break