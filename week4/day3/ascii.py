# Print a square pattern of asterisks
num_rows = int(input("Enter the number of rows: ")) # Get the number of rows from the user
for i in range(num_rows): # Iterate through each row
    for j in range(num_rows): # Iterate through each column
        print("*", end="")
    print()