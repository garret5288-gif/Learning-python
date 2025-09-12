# Prompt user for change owed until a positive float is provided
while True:
    try: # Try to convert input to float
        change = float(input("Change owed: "))
        if change > 0:
            break
        else: # Handle negative input
            print("Please enter a positive number.")
    except ValueError: # Handle non-numeric input
        print("Invalid input. Please enter a numeric value.")

# Convert dollars to cents to avoid floating point issues
cents = round(change * 100) # Convert dollars to cents
coins = 0
coin_values = [25, 10, 5, 1] # Coin denominations in cents

for coin in coin_values:
    coins += cents // coin # Use integer division to count coins
    cents %= coin # Update remaining cents

print(coins)