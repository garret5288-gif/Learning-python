# Define a Student class with attributes and methods

class Student: # Define Student class
    def __init__ (self, name, age): # Constructor with name and age
        self.name = name
        self.age = age

    def greet(self): # Method to greet
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

student1 = Student("Alice", 20) # Create instance

student1.greet()
print(f"Student Name: {student1.name}")