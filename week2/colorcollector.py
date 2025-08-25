colors = []
# Collect favorite colors from the user until they type "done".
while True:
    color = input("Enter a favorite color (or type done to finish): ")
    if color.lower() == "done":
        break
    colors.append(color)

print("Your favorite colors are:")
for c in colors:
    print("- " + c)