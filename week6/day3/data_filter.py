# data filtering module

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

def data_filter(data, threshold): # filter data based on threshold
    '''filter data to include only numbers >= threshold
    variables:
    data
    threshold
    returns: list of filtered numbers'''
    filtered = [i for i in data if i >= threshold] # List comprehension for filtering
    return filtered

def main(): # main function to run the data filter program
    data = collect_data()
    if not data: # Check if data is empty
        print("No data collected.")
        return
    while True:
        try: # Get threshold from user
            threshold = float(input("Enter threshold value: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    filtered_data = data_filter(data, threshold)
    print("Filtered data:", filtered_data) # Display filtered data

if __name__ == "__main__": # Entry point for the program
    main()