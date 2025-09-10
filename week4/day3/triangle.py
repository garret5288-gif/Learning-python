# triangle pattern
width = int(input("Enter the width of the triangle: ")) # asking for the total number or rows
for i in range(1, width + 1): # Adjusted so total wouldn't be excluded
    for j in range(1, i + 1): # For each iteration adds 1 more character
        print("*",end="") # Prints the number of *'s on the same line
    print() # Moves to next line

    