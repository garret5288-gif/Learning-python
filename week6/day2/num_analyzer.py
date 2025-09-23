# Number Analyzer

def collect_numbers(): # Collect numbers from user
    numbers = [] # Initialize empty list for numbers
    while True: # Loop to collect numbers
        num_input = input("Enter a number (or 'done' to finish): ")
        if num_input.lower() == 'done': # Check if user is done entering numbers
            break
        try: # Try to convert input to float
            number = float(num_input)
            numbers.append(number)
        except ValueError: # Handle non-numeric input
            print("Invalid input. Please enter a numeric value or 'done'.")
    return numbers

def analyze_numbers(numbers): # Analyze the list of numbers
    if not numbers: # Check if list is empty
        print("No numbers to analyze.")
        return
    print("Count:", len(numbers))
    print("Average:", sum(numbers) / len(numbers))
    print("Highest:", max(numbers))
    print("Lowest:", min(numbers))
    print("Sum:", sum(numbers))
    numbers_sorted = sorted(numbers) # Sort numbers for median calculation
    n = len(numbers_sorted)
    if n % 2 == 1: # Odd number of elements
        median = numbers_sorted[n // 2]
    else: # Even number of elements
        median = (numbers_sorted[n // 2 - 1] + numbers_sorted[n // 2]) / 2 # Average of two middle numbers
    print("Median:", median) # Median calculation

def main(): # Main function to run the number analyzer
    numbers = collect_numbers()
    analyze_numbers(numbers)