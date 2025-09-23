# manage a list with various operations

def main(): # Main function to run the list manager
    my_list = [] # Initialize empty list
    while True: # Main menu loop
        print("\nList Operations Menu")
        print("1. Append item")
        print("2. Insert item at position")
        print("3. Remove item by value")
        print("4. Pop last item")
        print("5. Sort list")
        print("6. Reverse list")
        print("7. Count occurrences of a value")
        print("8. View list")
        print("9. Exit")
        choice = input("Choose an option (1-9): ")

        if choice == '1': # Append item
            while True: # Loop to append items
                item = input("Enter item to append or 'done' to finish: ")
                if item.lower() == 'done':
                    break
                my_list.append(item)
        elif choice == '2': # Insert item at position
            item = input("Enter item to insert: ")
            while True: # Loop to get valid position
                pos_str = input("Enter position (0-based index): ")
                try: # Validate index input
                    pos = int(pos_str) # Convert to integer
                    if pos < 0 or pos > len(my_list): # Check range
                        print(f"Index out of range. Please enter 0 to {len(my_list)}.")
                        continue # Prompt again
                    my_list.insert(pos, item)
                    break
                except ValueError: # Handle non-integer input
                    print("Invalid index. Please enter an integer.")
        elif choice == '3':
            if not my_list: # Check if list is empty
                print("List is empty. Nothing to remove.")
            else:
                while True: # Loop to remove items
                    item = input("Enter item to remove or 'done' to finish: ")
                    if item.lower() == 'done':
                        break # Exit loop
                    if item in my_list: # Remove item if it exists
                        my_list.remove(item)
                    else: # Item not found
                        print("Item not found.")
        elif choice == '4':
            if my_list: # Pop last item if list is not empty
                print("Popped:", my_list.pop())
            else:
                print("List is empty.")
        elif choice == '5':
            my_list.sort() # Sort the list
            print("List sorted.")
            print("Current list:", my_list)
        elif choice == '6':
            my_list.reverse() # Reverse the list
            print("List reversed:", my_list)
        elif choice == '7':
            item = input("Enter value to count: ") # Count occurrences
            print(f"{item} appears {my_list.count(item)} times.")
        elif choice == '8': # View list
            print("Current list:", my_list)
        elif choice == '9': # Exit
            print("Goodbye!")
            break
        else: # Invalid choice
            print("Invalid choice.")

main() # Run the main function