product_names = []
categories = []
quantities = []

def add_product(name, category, quantity):
    if not name.strip():
        print("Product name cannot be empty.")
        return
    if not category.strip():
        print("Category cannot be empty.")
        return
    if not isinstance(quantity, int):
        print("Quantity must be an integer.")
        return
    if quantity < 0:
        print("Quantity cannot be negative.")
        return
    product_names.append(name)
    categories.append(category)
    quantities.append(quantity)

def update_quantity(name, quantity):
    if name in product_names:
        index = product_names.index(name)
        quantities[index] = quantity
    else:
        print(f"Product {name} not found.")

def view_inventory():
    print("Inventory:")
    for i in range(len(product_names)):
        print(f"Product: {product_names[i]}, Category: {categories[i]}, Quantity: {quantities[i]}")

def view_by_category(category):
    print(f"Products in category '{category}':")
    for i in range(len(product_names)):
        if categories[i] == category:
            print(f"Product: {product_names[i]}, Quantity: {quantities[i]}")

def clear_inventory():
    product_names.clear()
    categories.clear()
    quantities.clear()
    print("Cleared the inventory.")

def main():
    while True:
        print("\nInventory Manager:")
        print("1. Add Product")
        print("2. Update Quantity")
        print("3. View Inventory")
        print("4. View by Category")
        print("5. Clear Inventory")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            quantity = int(input("Enter product quantity: "))
            add_product(name, category, quantity)
        elif choice == "2":
            name = input("Enter product name: ")
            quantity = int(input("Enter new quantity: "))
            update_quantity(name, quantity)
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            category = input("Enter category: ")
            view_by_category(category)
        elif choice == "5":
            clear_inventory()
        elif choice == "6":
            print("Exiting Inventory Manager.")
            break
        else:
            print("Invalid choice. Please try again.")
main()