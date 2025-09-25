def create_board(rows, cols): # Create a game board with specified rows and columns
    return [["|   |" for _ in range(cols)] for _ in range(rows)] # Initialize board with empty cells

def print_board(board): # Print the game board
    for row in board: # Loop through each row
        print("-----" * len(row) + "-") # Print top border
        print("".join(row)) # Print row contents
        print("-----" * len(row) + "-") # Print bottom border

def main(): # Main function to create and display the board
    board = create_board(3, 3)  # Change 3, 3 to any size you want
    print_board(board) # Print the created board

main()
