# Simple phone book application
# Allows user to look up phone numbers by name

phone_book = { # Sample phone book data
    "Alice": "555-1234",
    "Bob": "555-5678",
    "Charlie": "555-8765",
    "Garret": "293-3223",
    "David": "555-4321",
    "Eve": "321-7654"
}

def show_available_contacts(): # Function to display available contacts
    print("Available contacts:")
    for name in phone_book.keys(): # Loop through names in phone book
        print(f"- {name}") # Print each name

def get_phone_number(): # Function to look up phone numbers
    print("Phone Book Lookup")
    print("=================")
    show_available_contacts()
    while True: # Loop to allow multiple lookups
        name = input("Enter the name to look up or 'quit' to exit: ")
        if name.lower() == 'quit': # Exit condition
            print("Exiting phone book lookup.")
            break
        if not name:
            print("Invalid input. Please enter a name.")
            continue
        # Use .get() for safe lookup, capitalize for consistency
        number = phone_book.get(name.capitalize())
        if number:
            print(f"{name.capitalize()}'s phone number is {number}")
        else:
            print("Name not found in phone book.")

get_phone_number()