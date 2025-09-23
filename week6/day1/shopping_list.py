# shopping list where you can add, remove, view, and clear items

shopping_list =[] # Initialize the shopping list
## Functions to manage the shopping list
def add_items(shopping_list):
    """Add multiple items to the shopping list."""
    while True: # Loop to add items
        item = input("Enter an item to add (or type 'done' to finish): ")
        if item.lower() == 'done' or item == '':
            break # Exit loop
        shopping_list.append(item) # Add item to list
        print(f'Added {item}. Current list: {shopping_list}')

def remove_item(shopping_list):
    """Remove an item from the shopping list if it exists."""
    while True: # Loop to remove items
        item = input("Enter an item to remove (or type 'done' to finish): ")
        if item.lower() == 'done' or item == '':
            break # Exit loop
        if item in shopping_list:
            shopping_list.remove(item) # Remove item from list
            print(f'Removed {item}. Current list: {shopping_list}')
        else: # Item not found
            print(f"{item} not found in the shopping list.")

def view_list(): # View the current shopping list
    """View the current shopping list."""
    if shopping_list:
        print("Current shopping list:")
        for idx, item in enumerate(shopping_list, start=1): # Enumerate items
            print(f"{idx}. {item}")
    else:
        print("The shopping list is empty.")

def clear_list(): # Clear the entire shopping list
    """Clear the entire shopping list."""
    shopping_list.clear()
    print("Cleared the shopping list.")

def main(): # Main menu loop
    while True:
        print("\nShopping List Menu:")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. View List")
        print("4. Clear List")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")
        # Handle user choices
        if choice == '1':
            add_items(shopping_list)
        elif choice == '2':
            remove_item(shopping_list)
        elif choice == '3':
            view_list()
        elif choice == '4':
            clear_list()
        elif choice == '5':
            print("Exiting the shopping list application.")
            break # Exit the program
        else: # Invalid choice
            print("Invalid choice. Please select a valid option.")

main()