# 3 diffent list comprehensions
# 1. Create a list of the cubes of all numbers in a given list.
# 2. Create a list of all even numbers from 0 to 50.
# 3. Create a list of all fruits from a given list that end with the letter

numbers = [1, 3, 5, 7, 9, 11, 13]
cubes = [x**3 for x in numbers] # List comprehension for cubes
print(cubes)  # Output: [1, 27, 125, 343, 729, 1331, 2197]

list1 = list(range(50)) # List of numbers from 0 to 49
evens = [x for x in list1 if x % 2 == 0] # List comprehension for evens
print(evens)  

fruits = ["apple", "banana", "cherry", "date", "fig", "grape"]
a_fruits = [fruit for fruit in fruits if fruit.endswith('e')] # List comprehension for fruits ending with 'e'
print(a_fruits) 