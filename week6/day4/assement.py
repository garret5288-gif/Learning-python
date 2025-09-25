# finding even numbers in a 2D list (matrix) and printing them

def find_evens(matrix):
    evens = []
    for row in matrix: # Iterate through each row
        for num in row: # Iterate through each number in the row
            if num % 2 == 0: # Check if the number is even
                evens.append(num) # Add even number to the list
    return evens

def print_evens(matrix): # Function to print even numbers from the matrix
    evens = find_evens(matrix)
    print("Even numbers in the matrix:", evens) # Print the list of even numbers

def main(): # Main function to run the program
    matrix = [ # Example 2D list (matrix)
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12]
    ]
    print_evens(matrix)

if __name__ == "__main__":
    main()