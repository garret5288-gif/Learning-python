personal_info = ("Garret", "Adkins", 37, "Male", "Single")

first_name = personal_info[0]
last_name = personal_info[1]
age = personal_info[2]
gender = personal_info[3]
marital_status = personal_info[4]   

print("\nPersonal Information:")
print("First Name:", first_name)
print("Last Name:", last_name)
print("Age:", age)
print("Gender:", gender)
print("Marital Status:", marital_status)

fruits = ["apple", "banana", "orange", "coconut", "mango"]

print()
print(fruits[2])  # Output: orange
print(fruits[-1]) # Output: mango
print(fruits[1:4]) # Output: ['banana', 'orange', 'coconut']
print(fruits[:3])  # Output: ['apple', 'banana', 'orange']
print(fruits[2:])  # Output: ['orange', 'coconut', 'mango']

fav_movies =["jurassic park", "the thing", "the matrix", "inception", "the godfather"]

print()
for movie in fav_movies:
    print(movie.title())
