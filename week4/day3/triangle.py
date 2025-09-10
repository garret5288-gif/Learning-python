# triangle pattern
width = int(input("Enter the width of the triangle: ")) # asking for the total number or rows
for i in range(width): 
    for j in range(i + 1): # For each iteration adds 1 more character
        print("*",end="") # Prints the number of *'s on the same line
    print() # Moves to next line

    