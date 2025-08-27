unit = input("Pick a unit km/h or mph: ").strip().lower()
if unit == 'km/h':
    value = float(input("Enter your speed in km/h: "))
    converted_value = value / 1.609
    print(f"{value} km/h is {round(converted_value, 2)} mph")
elif unit == 'mph':
    value = float(input("Enter your speed in mph: "))
    converted_value = value * 1.609
    print(f"{value} mph is {round(converted_value, 2)} km/h")
else:
    print("Invalid unit. Please enter 'km/h' or 'mph'.")    