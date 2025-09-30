# Simple price lookup system
# Allows user to check prices of products

product_prices = { # Sample product prices
    "apple": 0.60,
    "banana": 0.50,
    "orange": 0.75,
    "bacon": 5.00,
    "eggs": 3.00,
    "milk": 2.50,
    "bread": 2.00,
    "cheese": 4.00
}

def price_lookup(): # Function to look up product prices
    print("Welcome to the Price Lookup System!")
    print("Available products:")
    for item in product_prices.keys(): # Loop through product names
        print(f"- {item}")
    while True: # Loop to allow multiple lookups
        product = input("Enter the product name to check price or 'quit' to exit: ")
        if product.lower() == 'quit': # Exit condition
            print("Exiting price lookup.")
            return
        if not product: # Handle empty input
            print("Invalid input. Please enter a product name.")
            continue
        price = product_prices.get(product.lower()) # Get price or None if not found
        if price is not None:
            print(f"Price for {product}: ${price:.2f}")
        else:
            print(f"{product} not found in the price list.")
price_lookup()