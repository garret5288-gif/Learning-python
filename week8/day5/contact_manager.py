# contact manager with backup and restore

import json # for JSON handling
import os # for file operations

contacts_file = "contacts_main.json" # main contacts file

# --- Simple validation helpers ---
def normalize_name(name: str) -> str: # Normalize name to title case
    return " ".join(part.capitalize() for part in name.split())

def _digits_only(s: str) -> str: # helper to extract digits
    return "".join(ch for ch in s if ch.isdigit())

def is_valid_email(email: str) -> bool: # very basic check
    email = email.strip()
    if " " in email or "@" not in email:
        return False
    local, _, domain = email.partition("@")
    return bool(local) and "." in domain and domain[0] != "." and domain[-1] != "."

def is_valid_phone(phone: str) -> bool: # very basic check
    digits = _digits_only(phone)
    return 7 <= len(digits) <= 15  # simple length check

def is_duplicate(contacts, name: str, phone: str, email: str) -> bool: # check for duplicates
    name_l = name.strip().lower()
    phone_d = _digits_only(phone)
    email_l = email.strip().lower()
    for c in contacts: # check each contact
        cn = str(c.get('name','')).strip().lower()
        cp = _digits_only(str(c.get('phone','')))
        ce = str(c.get('email','')).strip().lower()
        if (cn == name_l and cp == phone_d) or (email_l and ce == email_l):
            return True
    return False

def menu(): # Display menu options
    print("Contact Manager")
    print("1. Add Contact")
    print("2. Remove Contact")
    print("3. View Contacts")
    print("4. Backup Contacts")
    print("5. Restore Contacts from Backup")
    print("6. Search Contacts")
    print("7. Exit")

def load_contacts(): # Load contacts from JSON file
    if not os.path.exists(contacts_file): # if file does not exist
        return []
    with open(contacts_file, "r", encoding="utf-8") as file:
        try: # ensure file operations are safe
            return json.load(file)
        except json.JSONDecodeError:
            print("Error reading contacts file. Starting with empty contact list.")
            return []

def save_contacts(contacts): # Save contacts to JSON file
    with open(contacts_file, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)
    print("Contacts saved.")

def add_contact(contacts): # Add a new contact
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email address: ").strip()
    if not name or not phone or not email: # validate input
        print("All fields are required.")
        return contacts
    if not is_valid_phone(phone):
        print("Phone looks invalid. Use at least 7 digits.")
        return contacts
    if not is_valid_email(email):
        print("Email looks invalid.")
        return contacts
    # Normalize name (title case); keep original phone/email formatting
    name = normalize_name(name)
    if is_duplicate(contacts, name, phone, email):
        print("Duplicate contact (same name+phone or email) not added.")
        return contacts
    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added.")
    return contacts

def remove_contact(contacts): # Remove a contact by number
    if not contacts: # Check if contact list is empty
        print("No contacts to remove.")
        return contacts
    for i, c in enumerate(contacts, 1): # display contacts with numbering
        name = c.get("name", "?")
        phone = c.get("phone", "?")
        email = c.get("email", "?")
        print(f"{i}. {name} | {phone} | {email}")
    choice = input("Enter the number of the contact to remove (or blank to cancel): ").strip()
    if not choice: # Cancel removal if input is blank
        print("Cancelled.")
        return contacts
    if not choice.isdigit() or not (1 <= int(choice) <= len(contacts)):
        print("Invalid choice.") # Validate user input
        return contacts
    index = int(choice) - 1 # Convert to 0-based index
    removed_contact = contacts.pop(index) # Remove the selected contact
    save_contacts(contacts)
    print(f"Removed contact: {removed_contact.get('name', '?')}")
    return contacts

def view_contacts(contacts): # View all contacts
    if not contacts: # Check if contact list is empty
        print("No contacts available.")
        return
    print("Contacts:")
    for i, c in enumerate(contacts, 1): # display contacts with numbering
        name = c.get("name", "?")
        phone = c.get("phone", "?")
        email = c.get("email", "?")
        print(f"{i}. {name} | {phone} | {email}")
    print()

def search_contacts(contacts): # Search contacts by field
    if not contacts:
        print("No contacts to search.")
        return
    print("Search by:") # Select the field to search by
    print("1. Name")
    print("2. Phone")
    print("3. Email")
    field_choice = input("Choose a field (1-3): ").strip()
    if field_choice not in {"1","2","3"}: # validate choice
        print("Invalid choice.")
        return
    query = input("Enter search text: ").strip() # get search text
    if not query: # validate query
        print("Search text cannot be empty.")
        return
    qn = query.lower()
    matches = [] # list of (index, name, phone, email) tuples
    for idx, c in enumerate(contacts, 1):
        name = str(c.get("name",""))
        phone = str(c.get("phone",""))
        email = str(c.get("email",""))
        target = ""
        if field_choice == "1":
            target = name
        elif field_choice == "2":
            target = phone
        else:
            target = email
        if qn in target.lower():
            matches.append((idx, name, phone, email))
    if not matches: # no matches found
        print("No matches found.")
        return
    print(f"Found {len(matches)} match(es):")
    for idx, name, phone, email in matches:
        print(f"{idx}. {name} | {phone} | {email}")
    print()

def backup_contacts(contacts): # Backup contacts to a separate file
    backup_file = "contacts_backup.json"
    try: # ensure file operations are safe
        with open(backup_file, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4)
        print(f"Contacts backed up to {backup_file}.")
    except OSError as e: # handle file errors
        print(f"Failed to backup contacts: {e}")

def restore_contacts(contacts): # Restore contacts from backup file
    backup_file = "contacts_backup.json"
    if not os.path.exists(backup_file): # if backup file does not exist
        print("No backup file found.")
        return contacts
    confirm = input("This will overwrite current contacts with the backup. Continue? (y/n): ").strip().lower()
    if confirm != 'y':  # Confirm before restoring
        print("Restore canceled.")
        return contacts
    try: # ensure file operations are safe
        with open(backup_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("Backup file format is invalid.")
            return contacts
        # Basic validation of items
        cleaned = [] # list of valid contacts
        for item in data: # only keep valid contact dicts
            if isinstance(item, dict) and {'name','phone','email'}.issubset(item.keys()):
                cleaned.append({
                    'name': str(item.get('name','')).strip(),
                    'phone': str(item.get('phone','')).strip(),
                    'email': str(item.get('email','')).strip(),
                })
        # Overwrite main contacts file
        with open(contacts_file, "w", encoding="utf-8") as out:
            json.dump(cleaned, out, indent=4)
        print(f"Restored {len(cleaned)} contacts from backup.")
        return cleaned
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to restore from backup: {e}")
        return contacts

def main(): # Main program loop
    contacts = load_contacts() # load existing contacts
    while True: # Main loop
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            contacts = add_contact(contacts)
        elif choice == "2":
            contacts = remove_contact(contacts)
        elif choice == "3":
            view_contacts(contacts)
        elif choice == "4":
            backup_contacts(contacts)
        elif choice == "5":
            contacts = restore_contacts(contacts)
        elif choice == "6":
            search_contacts(contacts)
        elif choice == "7":
            print("Exiting Contact Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()        
       
    