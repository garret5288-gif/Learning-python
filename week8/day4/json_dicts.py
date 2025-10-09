import json

people = [
    {"name": "Alice",
     "age": 30,
     "city": "New York"},
    {"name": "Bob",
     "age": 25,
     "city": "Los Angeles"},
    {"name": "Charlie",
     "age": 35,
     "city": "Chicago"}
]

with open("people.json", "w") as f:
    json.dump(people, f, indent=4)
    
with open("people.json", "r") as f:
    loaded_people = json.load(f)

print(loaded_people)
