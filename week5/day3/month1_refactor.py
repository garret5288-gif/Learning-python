# Refactored code for grade calculation with input validation
def validate_score(score_str): # Validate user input for score
    if not score_str.isdigit(): # Check if input is numeric
        print('Invalid input. Please enter a numeric value.')
        main() # Restart main function
        return None # Return None for invalid input
    score = int(score_str) # Convert to integer
    if 0 <= score <= 100:
        return score # Return valid score
    else:
        print('Invalid input. Please enter a score between 0 and 100.')
        main() # Restart main function
        return None

def get_grade(score): # Determine letter grade based on score
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
    
def main(): # Main function to run the program
    score_str = input("Enter your score (0-100): ")
    score = validate_score(score_str)
    if score is not None: # Proceed if score is valid
        grade = get_grade(score)
        print(f"Your grade is: {grade}")

main()