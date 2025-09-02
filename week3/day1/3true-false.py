def get_valid_age(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        else:
            print("Please enter a valid number for age.")

def get_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ['yes', 'no']:
            return value
        else:
            print("Please enter 'yes' or 'no'.")

age = get_valid_age('Enter your age: ')
citizen = get_yes_no('Are you a U.S. citizen? (yes/no): ')
married = get_yes_no('Are you married? (yes/no): ')

if age <= 18:
    print('You are not eligible to vote.')
else:
    print('You are eligible to vote.')

if citizen.lower() == 'yes':
    print('You are a citizen.')
else:
    print('You are not a citizen.')

if married.lower() == 'yes':
    print('You are married.')
else:
    print('You are not married.')