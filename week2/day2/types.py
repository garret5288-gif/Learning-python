name = "Garret"
age = 37
gpa = 3.5
student = True
print(type(name))  # <class 'str'>
print(type(age))   # <class 'int'>
print(type(gpa))   # <class 'float'>
print(type(student))  # <class 'bool'>

age = float(age)  # Convert age to float
print(age)
print(type(age))

gpa = int(gpa)  # Convert gpa to int
print(gpa)
print(type(gpa))

student = str(student)  # Convert student to string
print(student)
print(type(student))    

name = bool(name)  # Convert name to boolean
print(name)
print(type(name))
