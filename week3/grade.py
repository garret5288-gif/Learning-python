score = input('Enter your score: ')

if not score.isdigit():
    print('Invalid input. Please enter a numeric value.')
else:
    score = int(score)  
    if score < 0 or score > 100:
        print('Invalid input. Please enter a score between 0 and 100.')
    elif score >= 90:
        print('Grade: A')
    elif score >= 80:
        print('Grade: B')
    elif score >= 70:
        print('Grade: C')
    elif score >= 60:
        print('Grade: D')
    else:
        print('Grade: F')