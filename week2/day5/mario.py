# Get the height of the pyramid from the user
while True:
    height = (input("Enter the height of the pyramid (1-8): "))
    if height.isdigit(): # Check if input is a number
        height = int(height)
        if 1 <= height <= 8: # Check if height is between 1 and 8
            break
        else:
            print("Invalid input. Please enter a height between 1 and 8.") # Check if height is between 1 and 8
    else:
        print("Invalid input. Please enter a numeric value.") # Check if input is a number

for i in range(height): # Loop through each row
    print(" " * (height - i - 1) + "#" * (i + 1)) # Print each row of the pyramid
