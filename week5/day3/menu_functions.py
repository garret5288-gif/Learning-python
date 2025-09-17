def menu():
    while True:
        print("Menu:")
        print("1. Information")
        print("2. Help")
        print("3. Settings")
        print("4. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            option_1()
        elif choice == "2":
            option_2()
        elif choice == "3":
            option_3()
        elif choice == "4":
            option_4()
            break
        else:
            print("Invalid option. Please try again.")

def option_1():
    print("This is the Information section.")

def option_2():
    print("This is the Help section.")

def option_3():
    print("This is the Settings section.")

def option_4():
    print("Exiting the menu.")

menu()