import json # JSON serialization
import os # OS file operations

# Global in-memory catalog
products = []

class Product: # Product class with attributes and methods
    def __init__(self, name: str, price: float, quantity: int, category: str):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    @classmethod
    def get_product_count(cls): # Class method to get product count
        # Return current number of products tracked
        return len(products)

    def to_dict(self): # Convert product to dictionary for JSON serialization
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

    @staticmethod
    def from_dict(data: dict): # Create Product from dictionary
        return Product(
            name=data.get("name", ""),
            price=float(data.get("price", 0)),
            quantity=int(data.get("quantity", 0)),
            category=data.get("category", "")
        )
    
    def display_info(self): # Display product details
        print(f"Product: {self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}, Category: {self.category}")

def get_product_by_name(name: str): # Find product by name
    for p in products:
        if p.name.lower() == name.lower():
            return p
    return None

def add_product(name: str, price: float, quantity: int, category: str): # Add a new product
    if get_product_by_name(name): # prevent duplicates
        print(f"Product '{name}' already exists.")
        return
    new_product = Product(name, price, quantity, category)
    products.append(new_product) # add to list
    print(f"Added Product: {name}, Price: ${price:.2f}, Quantity: {quantity}, Category: {category}")
    save_products()

def save_products(): # Save products to JSON file
    try: # ensure file operations are safe
        data = [p.to_dict() for p in products]
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as e: # handle file errors
        print(f"Failed to save products: {e}")

def load_products(): # Load products from JSON file
    global products
    if not os.path.exists("products.json"):
        products = []
        return
    try: # ensure file operations are safe
        with open("products.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            products = [Product.from_dict(item) for item in data]
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to load products: {e}")
        products = []

def view_products(): # View all products
    if not products: # Check if product list is empty
        print("No products available.\n")
        return
    print("\nProduct Catalog:\n")
    for i, p in enumerate(products, 1): # display products with numbering
        print(f"{i}. ", end="")
        p.display_info()
    print()

def view_products_by_category(category: str): # View products filtered by category
    if not products:
        print("No products available.\n")
        return
    category = category.strip()
    if not category:
        print("Category cannot be blank.\n")
        return
    matches = [p for p in products if p.category.lower() == category.lower()]
    if not matches: # no matches found
        print(f"No products found in category '{category}'.")
        cats = sorted({p.category for p in products})
        if cats: # show available categories
            print("Available categories:")
            for c in cats:
                print(f"- {c}")
        print()
        return
    print(f"\nProducts in category: {category}\n")
    for i, p in enumerate(matches, 1):
        print(f"{i}. ", end="")
        p.display_info()
    print()

def remove_product(name: str): # Remove product by name
    global products
    before = len(products) # count before removal
    remaining = [p for p in products if p.name.lower() != name.lower()]
    if len(remaining) < before:
        removed = before - len(remaining) # number removed
        products = remaining
        print(f"Removed product '{name}'.")
        save_products()
    else: # no product found
        print(f"No product found with name '{name}'.")

def menu(): # Display menu options
    print("=== Product Catalog Menu ===")
    print("1. Add Product")
    print("2. Remove Product")
    print("3. View Products")
    print("4. Count Products")
    print("5. View by Category")
    print("6. Exit")
    print("============================")

def main(): # Main program loop
    load_products()
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = input("Enter product name: ").strip()
            price_raw = input("Enter product price: ").strip()
            quantity_raw = input("Enter product quantity: ").strip()
            category = input("Enter product category: ").strip()
            try:
                price = float(price_raw)
                quantity = int(quantity_raw)
                if price < 0 or quantity < 0:
                    raise ValueError
            except ValueError:
                print("Invalid price or quantity. Price must be a non-negative number and quantity a non-negative integer.\n")
                continue
            add_product(name, price, quantity, category)
        elif choice == "2":
            name = input("Enter product name to remove: ").strip()
            remove_product(name)
        elif choice == "3":
            view_products()
        elif choice == "4":
            print(f"Total Products: {Product.get_product_count()}\n")
        elif choice == "5":
            category = input("Enter category to view: ").strip()
            view_products_by_category(category)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()