import csv, os # for CSV handling and file ops

headers = ["item","quantity","price"] # CSV header fields

def ensure_header(path: str = "inventory.csv"): # Ensure CSV has header
    if not os.path.exists(path) or os.path.getsize(path) == 0: # file missing or empty
        with open(path, "w", newline="") as f: # open file for writing
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

def menu(): # Display menu options
    print("\n=== Inventory Menu ===\n")
    print("1. Add Inventory Item")
    print("2. View Inventory Items")
    print("3. Clear Inventory Items")
    print("4. Search Inventory Item")
    print("5. Update Item Quantity")
    print("6. Remove Item")
    print("7. Exit\n")

def add_inventory_item(): # Add a new inventory item
    ensure_header() # ensure header exists
    item = input("Enter item name: ").strip()
    quantity_raw = input("Enter quantity: ").strip()
    price_raw = input("Enter price: ").strip()
    if not item or not quantity_raw or not price_raw: # validate inputs
        print("All fields are required.\n")
        return
    if not quantity_raw.isdigit(): # quantity must be integer
        print("Quantity must be a non-negative integer.\n")
        return
    quantity = int(quantity_raw)
    try: # validate price
        price_val = float(price_raw)
        if price_val < 0: # price must be non-negative
            raise ValueError
    except ValueError: # validate price
        print("Price must be a non-negative number.\n")
        return
    with open("inventory.csv", "a", newline="") as csv_file: # append mode
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writerow({"item": item, "quantity": quantity, "price": f"{price_val:.2f}"})
    print("Inventory item added.\n")

def view_inventory_items(): # View all inventory items
    try: # Attempt to read inventory items
        with open("inventory.csv", "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            items = list(reader)
            if not items: # no items found
                print("No inventory items found.\n")
                return
            print("\nInventory Items:\n")
            total_value = 0.0 # total inventory value
            for i, row in enumerate(items, 1): # display items with numbering
                try: # parse quantity and price
                    q = int(row['quantity'])
                    p = float(row['price'])
                    total_value += q * p
                except (ValueError, KeyError): # handle parse errors
                    q = row.get('quantity')
                    p = row.get('price')
                print(f"{i}. Item: {row['item']}, Quantity: {row['quantity']}, Price: {row['price']}")
            print(f"\nTotal inventory value: {total_value:.2f}\n")
    except FileNotFoundError: # file does not exist
        print("No inventory items found.\n")

def clear_inventory_items(): # Clear all inventory items
    ensure_header()  # rewrites header
    with open("inventory.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
    print("Inventory cleared.\n")

def search_inventory_item(): # Search for an inventory item
    term = input("Enter search term: ").strip().lower() # case-insensitive
    try: # Attempt to read inventory items
        with open("inventory.csv", "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            results = [row for row in reader if term in row["item"].lower()]
            if not results: # no matches found
                print("No matching items found.\n")
                return
            print("\nSearch Results:\n")
            for i, row in enumerate(results, 1): # display results with numbering
                print(f"{i}. Item: {row['item']}, Quantity: {row['quantity']}, Price: {row['price']}")
            print()
    except FileNotFoundError: # file does not exist
        print("No inventory items found.\n")

def load_all_items() -> list[dict]: # Load all inventory items from CSV
    if not os.path.exists("inventory.csv"):
        return [] # no file
    with open("inventory.csv", "r", newline="") as f:
        reader = csv.DictReader(f) # read as dicts
        return list(reader)

def save_all_items(items: list[dict]): # Save all inventory items to CSV
    with open("inventory.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in items:
            writer.writerow(row)

def update_item_quantity(): # Update quantity of an existing item
    items = load_all_items() # load current items
    if not items: # no items
        print("No inventory items to update.\n")
        return
    # List items with index
    print("\nItems:")
    for i, r in enumerate(items, 1): # display with numbering
        print(f"{i}) {r['item']} (qty {r['quantity']})")
    choice = input("Select item number (blank cancels): ").strip()
    if not choice:  # Cancel if blank
        print("Cancelled.\n")
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
        print("Invalid selection.\n") # Handle invalid menu choices
        return
    idx = int(choice) - 1 # convert to 0-based index
    current = items[idx] # selected item
    new_q_raw = input(f"New quantity for {current['item']} (current {current['quantity']}): ").strip()
    if not new_q_raw.isdigit(): # validate new quantity
        print("Quantity must be a non-negative integer.\n")
        return
    current['quantity'] = new_q_raw # update quantity
    save_all_items(items) # save back to CSV
    print("Quantity updated.\n")

def remove_item(): # Remove an inventory item
    items = load_all_items() # load current items
    if not items: # no items
        print("No inventory items to remove.\n")
        return
    print("\nItems:")
    for i, r in enumerate(items, 1): # display with numbering
        print(f"{i}) {r['item']} (qty {r['quantity']})")
    choice = input("Select item number to remove (blank cancels): ").strip()
    if not choice:  # Cancel if blank
        print("Cancelled.\n")
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
        print("Invalid selection.\n") # Handle invalid menu choices
        return
    idx = int(choice) - 1 # convert to 0-based index
    removed = items.pop(idx)
    save_all_items(items) # save back to CSV
    print(f"Removed {removed['item']}.\n")

def main(): # Main program loop
    # Ensure the CSV file + header exist before any operations
    ensure_header()
    while True: # Loop until user chooses to exit
        menu()
        try:
            choice = input("Choose an option: ")
        except EOFError:
            # Gracefully handle unexpected end-of-input (e.g., Ctrl+D or piped input end)
            print("\nEOF received. Exiting...\n")
            break

        if choice == "1":
            add_inventory_item()
        elif choice == "2":
            view_inventory_items()
        elif choice == "3":
            clear_inventory_items()
        elif choice == "4":
            search_inventory_item()
        elif choice == "5":
            update_item_quantity()
        elif choice == "6":
            remove_item()
        elif choice == "7":
            print("Exiting...\n")
            break
        else: # Handle invalid menu choices
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()