from datetime import datetime

# getting user's birth date
birth_year = int(input('Enter your birth year (YYYY): '))
birth_month = int(input('Enter your birth month (MM): '))
birth_day = int(input('Enter your birth day (DD): '))

birth_date = datetime(birth_year, birth_month, birth_day)
today = datetime.today()

# calculating age based on today's date and birth date
age = today.year - birth_date.year
if (today.month, today.day) < (birth_date.month, birth_date.day):
    age -= 1

# displaying the calculated age to the user with spacing
print()
print(f"You are {age} years old.")
print()