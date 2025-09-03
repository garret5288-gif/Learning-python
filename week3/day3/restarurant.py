cuisine = input("Enter the cuisine type: ").strip()
price = input("Enter the price range (e.g., cheap, moderate, expensive): ").strip()
rating = float(input("Enter the rating (1-5): ").strip())

while True:
    if cuisine.isalpha() and price.isalpha() and (1 <= rating <= 5):
        break
    else:
        print("Invalid input. Please try again.")
        cuisine = input("Enter the cuisine type: ").strip()
        price = input("Enter the price range (e.g., cheap, moderate, expensive): ").strip()
        rating = float(input("Enter the rating (1-5): ").strip())

if cuisine.lower() == "italian" and (price.lower() == "moderate" and rating >= 4):
    print("You should try 'Luigi's Place'!")
elif cuisine.lower() == "japanese" and price.lower() == "expensive" and rating >= 4:
    print("You should try 'Sushi King'!")
elif cuisine.lower() == "mexican" and price.lower() == "cheap" and rating >= 3:
    print("You should try 'Taco Town'!")
elif cuisine.lower() == "indian" and price.lower() == "moderate" and rating >= 3:
    print("You should try 'Curry Palace'!")
elif cuisine.lower() == "american" and price.lower() == "cheap" and rating >= 3:
    print("You should try 'Burger Shanty'!")
elif cuisine.lower() == "chinese" and price.lower() == "moderate" and rating >= 4:
    print("You should try 'Panda Express'!")
elif cuisine.lower() == "mexican" and price.lower() == "expensive" and rating >= 4:
    print("You should try 'La Casa'!")
elif cuisine.lower() == "american" and price.lower() == "moderate" and rating >= 3:
    print("You should try 'Diner Deluxe'!")
elif cuisine.lower() == "italian" and price.lower() == "expensive" and rating >= 4:
    print("You should try 'Marios'!")
else:
    print("No recommendations available.")