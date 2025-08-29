colors = []
# Collect favorite colors from the user until they type "done".
while True: # Loop until user types "done"
    color = input("Enter a favorite color (or type done to finish): ")
    if color.lower() == "done":
        break
    colors.append(color) # Add color to the list
# Print the list of favorite colors.
print("Your favorite colors are:")
for c in colors:
    print("- " + c)