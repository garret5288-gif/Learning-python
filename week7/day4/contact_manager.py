import csv # For CSV file handling
import os # For file path handling

# Use a path relative to this script so it works on any machine
file_path = os.path.join(os.path.dirname(__file__), "contact.txt")
# You can change "contact.txt" to any desired filename
def load_contacts(file_path): # Load contacts from a CSV file
    """Load contacts from CSV (expects header: name,email,phone). Skips blank lines."""
    contacts = [] # List to hold contact dictionaries
    if not os.path.exists(file_path): # Check if file exists
        print("Contact file not found. Starting with an empty list.")
        return contacts # Return empty list if file doesn't exist
    try: # Open and read the CSV file
        with open(file_path, "r", newline="", encoding="utf-8") as file: # Open the file
            reader = csv.DictReader(file) # Create a DictReader
            for row in reader: # Iterate over each row
                if not row: # skip empty rows
                    continue
                name = (row.get("name") or "").strip()
                email = (row.get("email") or "").strip()
                phone = (row.get("phone") or "").strip()
                if not (name or email or phone):
                    # skip empty rows
                    continue
                contacts.append({"name": name, "email": email, "phone": phone})
    except Exception as e: # Handle file read errors
        print(f"Error reading contacts: {e}")
    return contacts

def save_contacts(file_path, contacts): # Save contacts to a CSV file
    """Save contacts to CSV with header."""
    try: # Open and write to the CSV file
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["name", "email", "phone"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for c in contacts: # Write each contact
                writer.writerow({
                    "name": (c.get("name") or "").strip(),
                    "email": (c.get("email") or "").strip(),
                    "phone": (c.get("phone") or "").strip(),
                })
        print(f"Saved {len(contacts)} contact(s) to {file_path}") # Log success
    except Exception as e: # Handle file write errors
        print(f"Error saving contacts: {e}")

def add_contact(contacts, name, email, phone): # Add a new contact
    contacts.append({"name": name, "email": email, "phone": phone})
    print(f"Contact {name} added.")
    return contacts

def list_contacts(contacts): # List all contacts
    if not contacts: # Check if the contact list is empty
        print("No contacts found.")
        return
    for i, contact in enumerate(contacts, 1): # Enumerate for numbering
        print(f"{i}. Name: {contact['name']}, Email: {contact['email']}, Phone: {contact['phone']}")

def search_contact(contacts, name): # Search for a contact by name
    for contact in contacts: # Iterate through contacts
        if contact['name'].lower() == name.lower(): # Case-insensitive match
            print(f"Found: Name: {contact['name']}, Email: {contact['email']}, Phone: {contact['phone']}")
            return
    print(f"Contact {name} not found.") # If not found

def delete_contact(contacts, name): # Delete a contact by name
    for i, contact in enumerate(contacts): # Iterate with index
        if contact['name'].lower() == name.lower(): # Case-insensitive match
            del contacts[i] # Delete the contact
            print(f"Contact {name} deleted.")
            return contacts
    print(f"Contact {name} not found.") # If not found
    return contacts 

def update_contact(contacts): # Update a contact by selecting its number
    """Update a contact selected by number. Press Enter to keep current value."""
    if not contacts: # Check if the contact list is empty
        print("No contacts to update.")
        return contacts
    list_contacts(contacts) # Show contacts to choose from
    choice = input("Enter the number of the contact to update: ").strip()
    if not choice.isdigit(): # Validate input
        print("Invalid selection.")
        return contacts
    idx = int(choice) - 1 # Convert to zero-based index
    if idx < 0 or idx >= len(contacts): # Check range
        print("Selection out of range.")
        return contacts
    c = contacts[idx] # Contact to update
    print("Press Enter to keep the current value shown in [brackets].")
    new_name = input(f"Name [{c['name']}]: ").strip()
    new_email = input(f"Email [{c['email']}]: ").strip()
    new_phone = input(f"Phone [{c['phone']}]: ").strip()
    if new_name: # Update name if provided
        c['name'] = new_name
    if new_email: # Update email if provided
        c['email'] = new_email
    if new_phone: # Update phone if provided
        c['phone'] = new_phone
    print("Contact updated.")
    return contacts

def main(): # Main program loop
    contacts = load_contacts(file_path)
    while True: # Main loop
        print("\nContact Manager")
        print("1. Add Contact")
        print("2. List Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Save Contacts")
        print("7. Reload From File")
        print("8. Exit")
        choice = input("Choose an option (1-8): ")
        
        if choice == '1': # Add contact
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            contacts = add_contact(contacts, name, email, phone)
            save_contacts(file_path, contacts)
        elif choice == '2': # List contacts
            list_contacts(contacts)
        elif choice == '3': # Search contact
            name = input("Enter name to search: ")
            search_contact(contacts, name)
        elif choice == '4': # Update contact
            contacts = update_contact(contacts)
            save_contacts(file_path, contacts)
        elif choice == '5': # Delete contact
            name = input("Enter name to delete: ")
            contacts = delete_contact(contacts, name)
            save_contacts(file_path, contacts)
        elif choice == '6': # Save contacts
            save_contacts(file_path, contacts)
        elif choice == '7': # Reload contacts
            contacts = load_contacts(file_path)
        elif choice == '8': # Exit
            print("Exiting Contact Manager.")
            break
        else: # Invalid option
            print("Invalid option. Please try again.")
if __name__ == "__main__":
    main()