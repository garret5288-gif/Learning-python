def collect_numbers():
    numbers = []
    while True:
        num_input = input("Enter")
        if num_input.lower() == 'done':
            break
        try:
            number = float(num_input)
            numbers.append(number)
        except ValueError:
            print("Invalid input. Please enter a numeric value or 'done'.")
    return numbers

def analyze_numbers(numbers):
    if not numbers:
        print("No numbers to analyze.")
        return
    print("Count:", len(numbers))
    print("Average:", sum(numbers) / len(numbers))
    print("Highest:", max(numbers))
    print("Lowest:", min(numbers))
    print("Sum:", sum(numbers))
    numbers_sorted = sorted(numbers)
    n = len(numbers_sorted)
    if n % 2 == 1:
        median = numbers_sorted[n // 2]
    else:
        median = (numbers_sorted[n // 2 - 1] + numbers_sorted[n // 2]) / 2
    print("Median:", median)

def main():
    numbers = collect_numbers()
    analyze_numbers(numbers)