# list transformation module
# This module provides functionality to transform a list of numbers.

def collect_data(): # collect user input
    '''collect numbers until 'done' is entered
    and handle invalid input
    variables: 
    entry
    num
    data
    returns: list of numbers'''
    data = [] # Initialize empty list
    while True: # Loop to collect data
        entry = input("Enter a number (or 'done' to finish): ")
        # Check for completion
        if entry.lower() == 'done':
            break
        try: # Try to convert input to float
            num = float(entry)
            data.append(num)
        except ValueError: # Handle invalid input
            print("Invalid input. Please enter a valid number.")
    return data

def list_transformer(data, factor): # transform list by multiplying each element by factor
    '''transform list by multiplying each element by factor
    variables:
    data
    factor
    returns: list of transformed numbers'''
    transformed = [i * factor for i in data] # List comprehension for transformation
    return transformed

def main(): # main function to run the list transformer program
    data = collect_data()
    if not data: # Check if data is empty
        print("No data collected.")
        return
    while True:
        try: # Get factor from user
            factor = float(input("Enter multiplication factor: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    transformed_data = list_transformer(data, factor)
    print("Transformed data:", transformed_data) # Display transformed data

if __name__ == "__main__": # Entry point for the program
    main()