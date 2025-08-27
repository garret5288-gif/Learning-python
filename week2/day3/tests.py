unit = input('Is this temperature (C/F): ').strip().lower()
temp = float(input('Enter the temperature: '))

if unit == 'c':
    temp = (temp * 9/5) + 32
    print(f'Temperature in Fahrenheit: {temp}')
elif unit == 'f':
    temp = (temp - 32) * 5/9
    print(f'Temperature in Celsius: {temp}')
else:
    print('Invalid unit')
