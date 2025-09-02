while True:
    password = input("Enter your password (at least 8 characters, including uppercase, lowercase, and a number): ").strip()
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
    elif not any(char.isupper() for char in password):
        print("Password must contain at least one uppercase letter.")
    elif not any(char.islower() for char in password):
        print("Password must contain at least one lowercase letter.")
    elif not any(char.isdigit() for char in password):
        print("Password must contain at least one number.")
    else:
        print("Password is valid.")
        break
