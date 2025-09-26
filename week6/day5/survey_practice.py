# survey practice
from collections import Counter

# Function to calculate average age
def average_age(all_responses):
    ages = [] # List to store ages
    for response in all_responses: # Loop through all responses
        try: # Try to convert age to integer
            ages.append(int(response[1])) # Assuming age is the second response
        except (ValueError, IndexError): # If conversion fails, skip this response
            continue
    if ages: # If we have valid ages
        avg = sum(ages) / len(ages) # Calculate average
        print(f"Average age: {avg:.1f}") # Print average age
    else:
        print("No valid ages to analyze.")

def most_common_color(all_responses): # Function to find the most common favorite color
    colors = [response[2].strip().lower() for response in all_responses if len(response) > 2]
    if colors: # If we have valid colors
        color_counts = Counter(colors) # Count occurrences of each color
        most_common = color_counts.most_common(1)[0][0] # Get the most common color
        print(f"Most common favorite color: {most_common}")
    else:
        print("No color data to analyze.")

def marital_status_count(all_responses): # Function to count marital statuses
    statuses = [response[5].strip().lower() for response in all_responses if len(response) > 5]
    if statuses: # If we have valid statuses
        status_counts = Counter(statuses) # Count occurrences of each status
        for status, count in status_counts.items(): # Loop through status counts
            print(f"{status.capitalize()}: {count}")
    else: # If we have no valid statuses
        print("No marital status data to analyze.")

def get_valid_age(prompt): # Function to get a valid age input
    while True: # Loop until valid input
        age = input(prompt) # Get user input
        if age.isdigit() and int(age) > 0: # Check if age is a valid positive integer
            return age
        print("Please enter a valid positive integer for age.")

def get_nonempty(prompt):
    while True: # Loop until valid input
        answer = input(prompt) # Get user input
        if answer.strip(): # Check if input is non-empty
            return answer
        print("Input cannot be empty.")

def get_status(prompt):
    while True: # Loop until valid input
        status = input(prompt + " (married/single): ").strip().lower()
        if status in ("married", "single"): # Check if input is valid
            return status
        print("Please enter 'married' or 'single'.")

def survey(questions, all_responses): # Function to conduct the survey
    print("\nNew Survey Participant (or type 'q' to quit):")
    responses = [] # List to store responses
    for question, validator in questions: # Loop through questions
        answer = validator(question) # Get validated answer
        if answer.lower() == 'q': # Check if user wants to quit
            return False
        responses.append(answer) # Add answer to responses
    all_responses.append(responses) # Add responses to all_responses
    return True

def view_results(questions, all_responses):
    if not all_responses: # Check if there are any responses
        print("No survey results yet.")
        return
    for idx, responses in enumerate(all_responses, 1):
        print(f"\nParticipant {idx}:") # Print participant number
        for (q, _), a in zip(questions, responses): # Loop through questions and responses
            print(f"{q} {a}")

def main():
    questions = [ # List of questions with their validators
        ("What is your name? ", get_nonempty),
        ("How old are you? ", get_valid_age),
        ("What is your favorite color? ", get_nonempty),
        ("Where were you born? ", get_nonempty),
        ("What is your favorite food? ", get_nonempty),
        ("Are you married or single?", get_status)
    ]
    all_responses = [] # List to store all participants' responses
    while True: # Loop for main menu
        print("\nSurvey Menu:")
        print("1. Take Survey")
        print("2. View Results")
        print("3. Analyze Data")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            while True: # Loop to take surveys
                if not survey(questions, all_responses):
                    break
                cont = input("Add another participant? (y/n): ")
                if cont.lower() != "y": # Check if user wants to add another participant
                    break
        elif choice == "2":
            view_results(questions, all_responses)
        elif choice == "3": # Analyze data
            print("\nAnalysis:")
            average_age(all_responses)
            most_common_color(all_responses)
            marital_status_count(all_responses)
        elif choice == "4": # Exit
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
