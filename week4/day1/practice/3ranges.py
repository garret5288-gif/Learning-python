def list(i): # Print numbers from 1 to i
    for i in range(1, i + 1): # Print numbers from 1 to 10
        print(i, end=" ")

def odd(i): # Print odd numbers from 1 to i
    for i in range(1, i + 1): # Print odd numbers from 1 to i
        if i % 2 != 0:
            print(i, end=" ")

def even(i):
    for i in range(1, i + 1):
        if i % 2 == 0: # Print even numbers from 1 to 
            print(i, end=" ")

if __name__ == "__main__":
    while True: # Loop until valid input is received
        num = input("Enter a number: ").strip()   
        if num == "":
            print("Enter a number")
        elif not num.isdigit():
            print("Enter a valid number")
        elif int(num) <= 0:
            print("Enter a number greater than 0")
        else: # Valid input received
            print("List of numbers from 1 to", num)
            list(int(num))
            print("\nList of odd numbers from 1 to", num)
            odd(int(num))
            print("\nList of even numbers from 1 to", num)
            even(int(num))
            break # Exit the loop after printing