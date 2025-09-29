# Simple inventory management system
# Allows user to check stock of products

inventory = { # Sample inventory data
    "apple": 50,
    "banana": 100,
    "orange": 75,
    "bacon": 25,
    "eggs": 200,
    "milk": 150,
    "bread": 80,
    "cheese": 60
}

def show_inventory(): # Function to display available products
    print("Available products:")
    for item in inventory.keys(): # Loop through product names
        print(f"- {item}") # Print each product name

def get_stock(): # Function to look up product stock
    print("Welcome to the Inventory Stock Checker!")
    show_inventory()
    while True: # Loop to allow multiple lookups
        product = input("Enter the product name to check stock or 'quit' to exit: ")
        if product.lower() == 'quit': # Exit condition
            print("Exiting stock check.")
            return
        if not product: # Handle empty input
            print("Invalid input. Please enter a product name.")
            continue
        stock = inventory.get(product.lower(), 0) # Get stock or 0 if not found
        print(f"Stock for {product}: {stock}") # Display stock


get_stock()
