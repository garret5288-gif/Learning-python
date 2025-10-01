# Survey Application
# Collects user responses to a set of questions and displays all results

def survey(): # Conduct the survey and collect responses
    survey_questions = [
        "What is your name?",
        "How old are you?",
        "What is your gender?",
        "What city were you born?",
        "What state do you live in?",
        "What is your favorite color?",
        "What is your favorite movie?"
    ]
    responses = {} # Dictionary to store responses
    for question in survey_questions: # Loop through each question
        answer = input(question + " ") # Get user input
        responses[question] = answer # Store the response
    return responses

def show_all_results(all_responses): # Display all survey results
    if not all_responses: # Check if there are any responses
        print("No survey responses yet.")
        return # Exit if no responses
    print("\nAll Survey Results:")
    for idx, responses in enumerate(all_responses, 1): # Enumerate through responses
        print(f"\nParticipant {idx}:") # Print participant number
        for question, answer in responses.items(): # Loop through each response
            print(f"{question} {answer}")

def main(): # Main function to run the survey application
    print("Survey Application")
    print("===================")
    all_responses = [] # List to store all participants' responses
    while True: # Main loop
        print("1. Take the survey")
        print("2. View all results")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            responses = survey() # Conduct the survey
            all_responses.append(responses) # Store the responses
            print("\nSurvey Responses:")
            for question, answer in responses.items(): # Display the responses
                print(f"{question} {answer}")
            print()
        elif choice == "2": 
            show_all_results(all_responses) # Show all collected results
        elif choice == "3": # Exit the program
            print("Exiting the survey application.")
            break
        else: # Invalid choice
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
