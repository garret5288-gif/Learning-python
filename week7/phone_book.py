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

def get_phone_number(): # Function to look up phone numbers
    print("Phone Book Lookup")
    print("=================")
    print("Available contacts: Alice, Bob, Charlie, Garret, David, Eve")
    while True: # Loop to allow multiple lookups
        name = input("Enter the name to look up or 'quit' to exit: ")
        if name.lower() == 'quit': # Exit condition
            print("Exiting phone book lookup.")
            break
        if name.capitalize() in phone_book: # Check if name exists
            print(f"{name}'s phone number is {phone_book[name.capitalize()]}") # Display phone number
        else: # Name not found case
            print("Name not found in phone book.")

get_phone_number()