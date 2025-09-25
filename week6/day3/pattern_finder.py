# pattern finder module     
# This module provides functionality to find patterns in a list of strings.

def collect_items():
    items = [] # Initialize empty list for items
    while True: # Loop to collect items
        entry = input("Enter an item (or type 'done' to finish): ")
        if entry.lower() == 'done' or entry == '': # Check for completion
            break # Exit loop
        items.append(entry) # Add item to list
    return items

def find_pattern(items, pattern): # find items matching the pattern
    matches = [item for item in items if pattern in item] # List comprehension for matching
    return matches

def main():
    items = collect_items()
    if not items: # Check if items list is empty
        print("No items collected.")
        return
    pattern = input("Enter a pattern to search for: ") # Get search pattern from user
    matched_items = find_pattern(items, pattern) # Find matching items
    if matched_items: # Check if any matches found
        print("Items matching the pattern:")
        for item in matched_items: # Iterate over matched items
            print(item)
    else:
        print("No items match the given pattern.")

if __name__ == "__main__":
    main()