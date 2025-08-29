# Menu
print("Menu:")
print("1. Hello World")
print("2. Help")
print("3. Bonus")

while True: # Loop until a valid choice is made
    choice = input("Enter your choice (1-3): ")
    if choice in ['1', '2', '3']: # Check if choice is valid
        break
    else:
        print("Invalid choice. Please select a valid option.")
# Execute the chosen option
if choice == '1':
    print("Hello, World!")
elif choice == '2':
    print("*****HELP*****")
    print("Never be afraid to ask for help when learning python!")
elif choice == '3':
    print("Bonus.")
    print("Congratulations on reaching the bonus section!")
