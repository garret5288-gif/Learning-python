# Example of list comprehension to double values greater than 5
stuff = [1, 2, 6, 9, 5]
results = [x * 2 for x in stuff if x > 5]
print(results)  # Output: [12, 18]