# created a Person class with attributes and methods
class Person: # Define Person class
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self): # Method to greet
        return f"Hello, my name is {self.name} and I am {self.age} years old."
# Create instances of Person
person1 = Person("John", 30)
person2 = Person("Jane", 25)
person3 = Person("Doe", 40)
# Use the greet method and print attributes
print(person1.greet())
print(person2.greet())
print(person3.greet())
print(f"Person 1: {person1.name}, Age: {person1.age}")
print(f"Person 2: {person2.name}, Age: {person2.age}")
print(f"Person 3: {person3.name}, Age: {person3.age}")