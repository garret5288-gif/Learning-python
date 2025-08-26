# This script converts lengths between feet and meters based on user input.
choice = input("Convert feet to meters (f) or meters to feet (m)? ").strip().lower()
if choice == 'f':
    feet = float(input("Enter length in feet: "))
    meters = feet * 0.3048  # 1 foot is 0.3048 meters
    print(f"{feet} feet is {round(meters, 2)} meters.")
elif choice == 'm':
    meters = float(input("Enter length in meters: "))
    feet = meters / 0.3048  # 1 meter is approximately 3.28084 feet
    print(f"{meters} meters is {round(feet, 2)} feet.")
else:
    print("Invalid choice. Please enter 'f' or 'm'.")  # Handle invalid user input