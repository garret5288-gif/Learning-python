# Simple configuration manager
# Allows user to set and get configuration settings
config = {} # Dictionary to store configuration settings

def set_config(key, value): # Function to set a configuration setting
    config[key] = value # Store the key-value pair
    print(f"Set {key} = {value}") # Confirm setting

def get_config(key): # Function to get a configuration setting
    value = config.get(key) # Retrieve the value for the given key
    if value is not None: # If the key exists, print the value
        print(f"{key} = {value}")
    else: # If the key does not exist, inform the user
        print(f"{key} not found in configuration.")

def main(): # Main function to run the configuration manager
    while True: # Loop to allow multiple operations
        print("\nConfiguration Manager")
        print("1. Set a setting")
        print("2. Get a setting")
        print("3. View all settings")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1": # Set a setting
            key = input("Enter setting name: ")
            value = input("Enter setting value: ")
            set_config(key, value)
        elif choice == "2": # Get a setting
            key = input("Enter setting name: ")
            get_config(key)
        elif choice == "3": # View all settings
            print("All settings:")
            for k, v in config.items():
                print(f"{k} = {v}")
        elif choice == "4": # Exit the program
            print("Exiting Configuration Manager.")
            break
        else: # If the choice is invalid
            print("Invalid choice. Please try again.")

main()
