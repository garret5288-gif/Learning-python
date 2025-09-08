

while True:
    num = input("Enter a number: ").strip()
    
    if num == "":
        print("Enter a number")
    elif not num.isdigit():
        print("Enter a valid number")
    elif int(num) <= 0:
        print("Enter a number greater than 0")
    else:
      for i in range(1, int(num) + 1, 2):
            print(i)
    break
