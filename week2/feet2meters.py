choice = input("Convert feet to meters (f) or meters to feet (m)? ")
if choice.lower() == 'f':
    feet = float(input("Enter length in feet: "))
    meters = feet * 0.3048
    print(f"{feet} feet is {meters} meters.")
elif choice.lower() == 'm':
    meters = float(input("Enter length in meters: "))
    feet = meters / 0.3048
    print(f"{meters} meters is {feet} feet.")
else:
    print("Invalid choice. Please enter 'f' or 'm'.")