# Print a star shape using nested loops
size = int(input("Enter the size of the star pattern: "))
for i in range(size):
    for j in range(size):
        if i == size // 2 or j == size // 2 or i == j or i + j == size - 1: # Print '*' at specific positions to form a star shape  
            print("*", end="")
        else:
            print(" ", end="") # Print space elsewhere
    print()