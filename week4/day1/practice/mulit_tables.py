# Print the multiplication table from 1 to 12
for i in range(1, 13): # Loop through numbers 1 to 12
    for j in range(1, 13): # Loop through numbers 1 to 12
        print(i * j, end="\t") # Print the product with a tab space
    print() # Newline after each row
