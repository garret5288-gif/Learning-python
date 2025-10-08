# save file processor
# A simple program to manage a text file: add, view, clear contents

import os

fake_file = "fake_file.txt" # File to manage

def ensure_file(): # Ensure the file exists
    if not os.path.exists(fake_file): # if file does not exist
        with open(fake_file, "w") as f: # create file
            f.write("This is a newly created file.\n")
        print(f"Created {fake_file} with default content.")

def add_to_file(text: str): # Add text to the file
    ensure_file()
    with open(fake_file, "a") as file:
        file.write(text + "\n")
    print(f"Added to {fake_file}.")

def clear_file(): # Clear the file contents
    ensure_file()
    with open(fake_file, "w") as file:
        pass  # Clear the file
    print(f"Cleared {fake_file}.")

def view_file(): # View the file contents
    ensure_file()
    with open(fake_file, "r") as file: # open for reading
        content = file.read()
    print(f"Contents of {fake_file}:") 
    print(content if content.strip() else "(empty)")

def menu(): # Display menu options
    print("1. Add to file")
    print("2. View file")
    print("3. Clear file")
    print("4. Exit")

def main(): # Main program loop
    ensure_file()
    while True: # Loop until user chooses to exit
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            text = input("Enter text to add: ").strip()
            if text:
                add_to_file(text)
            else:
                print("No text entered.")
        elif choice == "2":
            view_file()
        elif choice == "3":
            clear_file()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()