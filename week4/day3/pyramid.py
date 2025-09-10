# This program prints a pyramid pattern based on user-defined width
width = int(input("Enter the width of the pyramid: "))
for i in range(width + 1): 
    for j in range(width - i): # Print leading spaces
        print(" ", end="")
    for k in range(2 * i - 1): # Print stars
        print("*", end="")
    print() # Move to the next line after each row
