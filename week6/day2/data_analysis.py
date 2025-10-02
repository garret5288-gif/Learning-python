def collect_data():
    data = []
    while True:
        entry = input("Enter data (or type 'done' to finish): ")
        if entry.lower() == 'done' or entry == '':
            break
        try:
            value = float(entry)
            data.append(value)
        except ValueError:
            print("Please enter a valid number.")
    return data

def menu():
    print("\nData Analysis Menu")
    print("1. View Data")
    print("2. Sum")
    print("3. Average")
    print("4. Minimum")
    print("5. Maximum")
    print("6. Median")
    print("7. Count")
    print("8. Sort Data")
    print("9. Search Value")
    print("10. Exit")

def median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n == 0:
        return None
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        mid1 = sorted_data[n // 2 - 1]
        mid2 = sorted_data[n // 2]
        return (mid1 + mid2) / 2

def main():
    data = collect_data()
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Data:", data)
        elif choice == "2":
            print("Sum:", sum(data))
        elif choice == "3":
            print("Average:", sum(data) / len(data) if data else 0)
        elif choice == "4":
            print("Minimum:", min(data) if data else None)
        elif choice == "5":
            print("Maximum:", max(data) if data else None)
        elif choice == "6":
            print("Median:", median(data))
        elif choice == "7":
            print("Count:", len(data))
        elif choice == "8":
            print("Sorted Data:", sorted(data))
        elif choice == "9":
            value = float(input("Enter value to search: "))
            print("Search Result:", "Found" if value in data else "Not Found")
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

main()