print("Menu:")
print("1. Hello World")
print("2. Help")
print("3. Bonus")

while True:
    choice = input("Enter your choice (1-3): ")
    if choice in ['1', '2', '3']:
        break
    else:
        print("Invalid choice. Please select a valid option.")

if choice == '1':
    print("Hello, World!")
elif choice == '2':
    print("*****HELP*****")
elif choice == '3':
    print("Bonus.")
else:
    print("Invalid choice. Please select a valid option.")