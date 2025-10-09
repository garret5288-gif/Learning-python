import json

# Simple contact database application
# Allows users to add, view, save, and load contacts stored in a JSON file.

def menu(): # Display menu options
    print("Contact Database Menu")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Save Contacts to File")
    print("4. Load Contacts from File")
    print("5. Exit")

def add_contact(contacts): # Add a new contact
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email address: ").strip()
    if not name or not phone or not email: # validate input
        print("All fields are required.\n")
        return
    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact) # add to list
    print("Contact added (not yet saved).\n")

def view_contacts(contacts): # View all contacts
    if not contacts:
        print("\nNo contacts in memory. Use option 1 to add or option 4 to load from file.\n")
        return
    print("\nContacts:")
    for i, c in enumerate(contacts, 1): # display contacts with numbering
        name = c.get("name", "?")
        phone = c.get("phone", "?")
        email = c.get("email", "?")
        print(f"{i}. {name} | {phone} | {email}")
    print()

def save_contacts(contacts): # Save contacts to JSON file
    try: # ensure file operations are safe
        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)
        print("Contacts saved to contacts.json.\n")
    except OSError as e: # handle file errors
        print(f"Failed to save contacts: {e}\n")

def load_contacts(): # Load contacts from JSON file
    try: # ensure file operations are safe
        with open("contacts.json", "r", encoding="utf-8") as file: # Open file for reading
            contacts = json.load(file) 
        print(f"Loaded {len(contacts)} contacts from contacts.json.\n")
        return contacts
    except FileNotFoundError: # file does not exist
        print("No saved contacts found.\n")
        return []
    except json.JSONDecodeError: # handle JSON errors
        print("Error reading contacts file. Starting with empty contact list.\n")
        return []
    
def main(): # Main program loop
    contacts = []
    while True: # Main loop
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            save_contacts(contacts)
        elif choice == "4":
            contacts = load_contacts()
        elif choice == "5":
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()