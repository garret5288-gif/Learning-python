x = (input("Enter a number for x: ").strip())
y = (input("Enter a number for y: ").strip())

while True:
    if x.isdigit() and y.isdigit():
        x = int(x)
        y = int(y)
        break
    else:
        print("Invalid input. Please enter valid numbers.")
        x = (input("Enter a number for x: ").strip())
        y = (input("Enter a number for y: ").strip())

if x < y:
    print("x is less than y")
elif x == y:
    print("x is equal to y")
else:
    print("x is greater than y")
