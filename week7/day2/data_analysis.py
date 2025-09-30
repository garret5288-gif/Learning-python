# Sample sales data
# Analyzes sales performance of products

sales = { # Sample sales data
    "Apple": 100,
    "Banana": 65,
    "Orange": 20,
    "Grapes": 75,
    "Mango": 30,
    "Pineapple": 35,
    "Strawberry": 40,
    "Blueberry": 50,
}

def analyze_sales(sales_data): # Function to analyze sales data
    print("Sales Data Analysis")
    print("---------------------")
    for product, sales in sales_data.items(): # Iterating through products and their sales
        print(f"- {product}: {sales} units sold")
    total_sales = sum(sales_data.values()) # Total sales calculation
    average_sales = total_sales / len(sales_data) # Average sales calculation
    max_product = max(sales_data, key=sales_data.get) # Product with highest sales
    min_product = min(sales_data, key=sales_data.get) # Product with lowest sales

    print(f"Total Sales: {total_sales}")
    print(f"Highest Selling Product: {max_product} with {sales_data[max_product]} units sold")
    print(f"Lowest Selling Product: {min_product} with {sales_data[min_product]} units sold")
    print(f"Average Sales: {average_sales:.2f}")

analyze_sales(sales)