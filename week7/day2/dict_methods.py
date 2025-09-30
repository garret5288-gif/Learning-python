# Demonstrating dictionary methods: keys(), values(), and items()

name_age = {"Alice": 30,
             "Bob": 25, 
             "Charlie": 35,
             "Garret": 37,
             "David": 28
             }

print(name_age.keys())  # dict_keys(['Alice', 'Bob', 'Charlie', 'Garret', 'David'])
print(name_age.values()) # dict_values([30, 25, 35, 37, 28])
print(name_age.items())  # dict_items([('Alice', 30), ('Bob', 25), ('Charlie', 35), ('Garret', 37), ('David', 28)])