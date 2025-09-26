# Inventory Manager
# This program manages an inventory of products using parallel lists.

product_names = [] # List to store product names
categories = [] # List to store product categories
quantities = [] # List to store product quantities

def sort_by_name(item): # Function to sort by product name
    return str(item[0]).lower()

def sort_by_category(item): # Function to sort by product category
    return str(item[1]).lower()

def sort_by_quantity(item): # Function to sort by product quantity
    return int(item[2])

def sort_inventory(by="name"): # Function to sort inventory
    global product_names, categories, quantities
    combined = list(zip(product_names, categories, quantities)) # Combine parallel lists
    if by == "name":
        combined.sort(key=sort_by_name)
    elif by == "category":
        combined.sort(key=sort_by_category)
    elif by == "quantity":
        combined.sort(key=sort_by_quantity)
    if combined: # Update global lists if combined is not empty
        product_names, categories, quantities = map(list, zip(*combined))
    print(f"Inventory sorted by {by}.")
    print("Sorted Inventory:")
    for i in range(len(product_names)):
        print(f"Product: {product_names[i]}, Category: {categories[i]}, Quantity: {quantities[i]}")

def add_product(name, category, quantity): # Function to add a product
    if name in product_names: # Check for duplicate product names
        print(f"Product '{name}' already exists.")
        return False # Indicate failure to add
    product_names.append(name) # Add product details to lists
    categories.append(category) # Add category
    quantities.append(quantity) # Add quantity
    print(f"Product '{name}' added successfully.")
    return True # Indicate successful addition

def update_quantity(name, quantity): # Function to update product quantity
    if name not in product_names: # Check if product exists
        print(f"Product {name} not found.")
        return # Indicate failure to update
    if not isinstance(quantity, int) or quantity < 0:
        print("Quantity must be a non-negative integer.")
        return # Validate quantity
    index = product_names.index(name) # Find product index
    quantities[index] = quantity # Update quantity
    print(f"Updated {name} quantity to {quantity}.")

def view_inventory(): # Function to view the entire inventory
    print("Inventory:")
    for i in range(len(product_names)): # Loop through all products
        print(f"Product: {product_names[i]}, Category: {categories[i]}, Quantity: {quantities[i]}")

def search_product(name): # Function to search for a product by name
    if name in product_names: # Check if product exists
        index = product_names.index(name) # Find product index
        print(f"Product: {product_names[index]}, Category: {categories[index]}, Quantity: {quantities[index]}")
    else: # Product not found
        print(f"Product {name} not found.")

def clear_inventory(): # Function to clear the entire inventory
    product_names.clear()
    categories.clear()
    quantities.clear()
    print("Cleared the inventory.")

def search_by_category(category): # Function to search products by category
    found = False # Flag to track if any product is found
    for i in range(len(product_names)): # Loop through all products
        if categories[i].lower() == category.lower(): # Case-insensitive match
            print(f"Product: {product_names[i]}, Category: {categories[i]}, Quantity: {quantities[i]}")
            found = True # Mark as found
    if not found: # No products found in the category
        print(f"No products found in category {category}.")

def get_name(prompt): # Function to get a valid product name
    while True:
        name = input(prompt).strip()
        if name:
            return name
        print("Input cannot be empty.")

def get_category(prompt): # Function to get a valid category
    while True:
        category = input(prompt).strip()
        if category:
            return category
        print("Category cannot be empty.")

def get_quantity(prompt): # Function to get a valid quantity
    while True:
        try:
            quantity = int(input(prompt))
            if quantity >= 0:
                return quantity
            else:
                print("Quantity must be a non-negative integer.")
        except ValueError: # Handle non-integer input
            print("Please enter a valid integer for quantity.")

def main(): # Main menu loop
    while True:
        print("Inventory Manager")
        print("1. Add Product")
        print("2. Update Quantity")
        print("3. View Inventory")
        print("4. Clear Inventory")
        print("5. Search Product")
        print("6. Search by Category")
        print("7. Sort Inventory")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            while True: # Loop to add multiple products
                name = get_name("Enter product name (or 'q' to stop): ")
                if name.lower() == "q": # Check for quit signal
                    break
                category = get_category("Enter product category: ")
                quantity = get_quantity("Enter product quantity: ")
                add_product(name, category, quantity)
        elif choice == "2":
            name = input("Enter product name: ")
            quantity = get_quantity("Enter new quantity: ")
            update_quantity(name, quantity)
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            clear_inventory()
        elif choice == "5":
            name = input("Enter product name to search: ")
            search_product(name)
        elif choice == "6":
            category = input("Enter category to search: ")
            search_by_category(category)
        elif choice == "7":
            while True: # Loop to get valid sort option
                print("Sort by: 1. Name  2. Category  3. Quantity")
                sort_choice = input("Enter choice: ")
                if sort_choice == "1":
                    sort_inventory("name")
                    break
                elif sort_choice == "2":
                    sort_inventory("category")
                    break
                elif sort_choice == "3":
                    sort_inventory("quantity")
                    break
                else: # Invalid sort option
                    print("Invalid sort option. Please enter 1, 2, or 3.")
        elif choice == "8": # Exit option
            print("Exiting Inventory Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

main() # Run the main function to start the program