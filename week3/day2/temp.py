while True:
    temp = input("Enter the temperature in Fahrenheit: ")
    if temp.lstrip('-').isdigit():
        temp = int(temp)
        break
    else:
        print("Invalid input. Please enter a numeric temperature.")

if temp > 85:
    print("It's hot outside!")
    print("Wear light clothing.")
elif temp < 60:
    print("It's cold outside!")
    print("Wear warm clothing.")
else:
    print("The weather is mild.")
