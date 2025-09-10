# muliplication table base on user input
num = int(input("What should number should your table go to: "))

for i in range(1, num + 1): # iterate through rows
    for j in range(1, num +1): # iterate through columns
        print(i * j, end="\t") 
    print() # print a new line after each row

