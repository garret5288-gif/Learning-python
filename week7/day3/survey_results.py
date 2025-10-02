def survey():
    survey_questions = [
    "What is your name?",
    "How old are you?",
    "What is your gender?",
    "What city were you born?",
    "What state do you live in?",
    "What is your favorite color?",
    "What is your favorite movie?"
]
    responses = {}
    for question in survey_questions:
        answer = input(question + " ")
        responses[question] = answer
    return responses

def main():
    print("Survey Application")
    print("===================")
    while True:
        print("1. Take the survey")
        print("2. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            responses = survey()
            print("\nSurvey Responses:")
            for question, answer in responses.items():
                print(f"{question} {answer}")
            print()
        elif choice == "2":
            print("Exiting the survey application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
