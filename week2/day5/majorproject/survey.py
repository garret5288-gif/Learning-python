# Survey Introduction
print("*****SURVEY*****")
print("Please answer the following questions:")

def get_alpha_input(prompt): # Get a non-empty alphabetic string from the user
    while True:
        value = input(prompt).strip().capitalize()
        if value and value.isalpha(): # Check if input is not empty and contains only letters
            return value
        print("Input cannot be empty and must contain only letters. Please try again.")

def get_noempty_input(prompt): # Get a non-empty string from the user
    while True:
        value = input(prompt).strip().title()  
        if value: # Check if input is not empty
            return value
        else:
            print("Input cannot be empty. Please try again.")

def get_valid_age(prompt): # Get a valid age from the user
    while True:
        age = input(prompt).strip()
        if age.isdigit() and 0 < int(age) < 120: # Check if age is a valid number
            return int(age)
        print("Please enter a valid age (between 1 and 119).")
# Get survey responses
name = get_alpha_input("What is your first name? ")
age = get_valid_age("How old are you? ")
favorite_color = get_noempty_input("What is your favorite color? ")
favorite_food = get_noempty_input("What is your favorite food? ")
birth_city = get_noempty_input("What city were you born in? ")

# Survey Summary
print('Survey Results:\n')
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Favorite Color: {favorite_color}")
print(f"Favorite Food: {favorite_food}")
print(f"City Of Birth: {birth_city}")