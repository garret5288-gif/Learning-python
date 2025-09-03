
print("Trip Planner:\n")
print("What's your transportation mode?")
print("1. Car")
print("2. Train")
print("3. Plane")



while True:
    choice_1 = input("Enter your choice (1-3): ").strip()
    if choice_1 in ["1", "2", "3"]:
        break
    print("Invalid choice. Please try again.")

if choice_1 == "1":
    print("You have chosen Car. What is your budget?")
    print("1. Low")
    print("2. Medium")
    print("3. High")
   
    while True:
        choice_2 = input("Enter your choice (1-3): ").strip()
        if choice_2 in ["1", "2", "3"]:
            break
        print("Invalid choice. Please try again.")

    if choice_2 == "1":
        print("You have a low budget for your Car trip.")
    elif choice_2 == "2":
        print("You have a medium budget for your Car trip.")
    elif choice_2 == "3":
        print("You have a high budget for your Car trip.")
    else:
        print("Invalid choice.")

elif choice_1 == "2":
    print("You have chosen Train. What is your budget?")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    while True:
        choice_2 = input("Enter your choice (1-3): ").strip()
        if choice_2 in ["1", "2", "3"]:
            break
        print("Invalid choice. Please try again.")

    if choice_2 == "1":
        print("You have a low budget for your Train trip.")
    elif choice_2 == "2":
        print("You have a medium budget for your Train trip.")
    elif choice_2 == "3":
        print("You have a high budget for your Train trip.")
    else:
        print("Invalid choice.")
elif choice_1 == "3":
    print("You have chosen Plane. What is your budget?")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    while True:
        choice_2 = input("Enter your choice (1-3): ").strip()
        if choice_2 in ["1", "2", "3"]:
            break
        print("Invalid choice. Please try again.")

    if choice_2 == "1":
        print("You have a low budget for your Plane trip.")
    elif choice_2 == "2":
        print("You have a medium budget for your Plane trip.")
    elif choice_2 == "3":
        print("You have a high budget for your Plane trip.")
    else:
        print("Invalid choice.")
else:
    print("Invalid choice.")

