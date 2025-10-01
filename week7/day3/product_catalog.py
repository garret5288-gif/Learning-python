# Product Catalog Application
# Allows users to view products by category or all products

product_catalog = { # Sample product catalog data
    "Fruit": { "Apple": 50, "Banana": 30, "Orange": 20, "Grapes": 40, "Mango": 25 },
    "Vegetables": { "Carrot": 15, "Broccoli": 20, "Spinach": 10, "Potato": 25, "Tomato": 15 },
    "Dairy": { "Milk": 60, "Cheese": 40, "Yogurt": 30, "Butter": 25, "Cream": 20 },
    "Meat": { "Chicken": 70, "Beef": 90, "Pork": 80, "Lamb": 100, "Fish": 60 }
}

def display_catalog(catalog): # Function to display products in the catalog
    for category, items in catalog.items(): # Iterate through categories
        print(f"\nCategory: {category}") # Print category name
        for product, qty in items.items(): # Iterate through products
            print(f" - {product}: quantity {qty}") # Print product and quantity

def main(): # Main function to run the product catalog application
    categories = list(product_catalog.keys()) # List of categories
    while True: # Loop to allow multiple views
        print("\nWelcome to the Product Catalog")
        for i, category in enumerate(categories, 1): # Display categories with numbers
            print(f"{i}. {category}")
        print(f"{len(categories)+1}. View all") # Option to view all products
        print(f"{len(categories)+2}. Exit") # Option to exit
        choice = input("Enter number to view products: ")
        if choice == str(len(categories)+2): # Exit condition
            print("Exiting the product catalog.")
            break
        elif choice == str(len(categories)+1): # View all products
            display_catalog(product_catalog)
        elif choice.isdigit() and 1 <= int(choice) <= len(categories): # Valid category choice
            selected = categories[int(choice)-1] # Get selected category
            display_catalog({selected: product_catalog[selected]}) # Display selected category
        else: # Invalid choice
            print("Invalid choice. Please enter a valid number.")

if __name__ == "__main__":
    main()
