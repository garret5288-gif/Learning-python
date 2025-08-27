user_name = input("Enter your username: ").strip().lower()# Remove leading/trailing whitespace and convert to lowercase
city = input("Enter your city: ").strip().capitalize()# Remove leading/trailing whitespace and convert to capitalize
school = input("Enter the school you graduated from: ").strip().title()# Remove leading/trailing whitespace and convert to title case
print(f"Hello, {user_name} from {city}, graduate of {school}!")# Print everything with proper formatting
