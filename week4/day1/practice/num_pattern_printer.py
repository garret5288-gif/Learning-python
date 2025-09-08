# num_pattern_printer.py

while True: # Loop until valid input is received
    num = input("Enter a number: ").strip()   
    if num == "":
        print("Enter a number")
    elif not num.isdigit():
        print("Enter a valid number")
    elif int(num) <= 0:
        print("Enter a number greater than 0")
    else: # Valid input received
        for i in range(1, int(num) + 1, 2): # Print odd numbers from 1 to num
            print(i)
        break # Exit the loop after printing