def word_count(text):
    return len(text.split())

def char_count(text):
    return len(text)

def space_count(text):
    return text.count(' ')

def get_user_input():
    return input("Enter your text: ")


def display_menu():
    text = get_user_input()
    while True:
        print("1. Word Count")
        print("2. Character Count")
        print("3. Space Count")
        print("4. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            print(f"Word Count: {word_count(text)}")
        elif choice == "2":
            print(f"Character Count: {char_count(text)}")
        elif choice == "3":
            print(f"Space Count: {space_count(text)}")
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

display_menu()