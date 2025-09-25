# Simple Survey Analyzer

def run_survey():
    questions = [ # List of survey questions
        "What is your name? ",
        "What is your favorite color? ",
        "How old are you? ",
        "Are you male or female? ",
        "What is your favorite movie? ",
        "What is your favorite book? ",
        "Are you single or married? "
    ]
    responses = [] # List to store responses
    for question in questions: # Loop through each question
        answer = input(question + " ") # Get user input
        responses.append(answer) # Store response
    
    print("\nSurvey Results:")
    for i in range(len(questions)): # Loop through questions and responses
        print(f"{questions[i]}: {responses[i]}") # Print question and corresponding response

run_survey() # Run the survey function