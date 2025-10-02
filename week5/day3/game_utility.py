import random

def roll_dice(sides=10):
    return random.randint(1, sides)

def calculate_score(rolls):
    return sum(rolls)


