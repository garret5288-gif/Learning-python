# This script converts lengths between feet and meters based on user input.
choice = input("Convert feet to meters (f) or meters to feet (m)? ")
if choice.lower() == 'f':
    feet = float(input("Enter length in feet: "))
    meters = feet * 0.3048  # 1 foot is 0.3048 meters
    print(f"{feet} feet is {meters} meters.")
elif choice.lower() == 'm':
    meters = float(input("Enter length in meters: "))
    feet = meters / 0.3048  # 1 meter is approximately 3.28084 feet
    print(f"{meters} meters is {feet} feet.")
else:
    print("Invalid choice. Please enter 'f' or 'm'.")  # Handle invalid user input