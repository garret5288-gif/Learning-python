# if greeting starts with "hello" (case insensitive), output $0
# if greeting starts with "h" (case insensitive), output $20
# otherwise, output $100
greeting = input("Greeting: ").strip().lower()
if greeting.startswith("hello"): # checking if the string starts with hello
    print("$0")
elif greeting.startswith("h"): # checking if the string starts with h
    print("$20")
else:
    print("$100")