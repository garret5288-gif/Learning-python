from collections import Counter

def average_age(all_responses):
    ages = []
    for response in all_responses:
        try:
            ages.append(int(response[1]))  # Age is the second question
        except (ValueError, IndexError):
            continue
    if ages:
        avg = sum(ages) / len(ages)
        print(f"Average age: {avg:.1f}")
    else:
        print("No valid ages to analyze.")

def most_common_color(all_responses):
    colors = [response[2].strip().lower() for response in all_responses if len(response) > 2]
    if colors:
        color_counts = Counter(colors)
        most_common = color_counts.most_common(1)[0][0]
        print(f"Most common favorite color: {most_common}")
    else:
        print("No color data to analyze.")

def marital_status_count(all_responses):
    statuses = [response[6].strip().lower() for response in all_responses if len(response) > 6]
    if statuses:
        status_counts = Counter(statuses)
        for status, count in status_counts.items():
            print(f"{status.capitalize()}: {count}")
    else:
        print("No marital status data to analyze.")

def get_valid_age(prompt):
    while True:
        age = input(prompt)
        if age.isdigit() and int(age) > 0:
            return age
        print("Please enter a valid positive integer for age.")

def get_nonempty(prompt):
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("Input cannot be empty.")

def get_status(prompt):
    while True:
        status = input(prompt + " (married/single): ").strip().lower()
        if status in ("married", "single"):
            return status
        print("Please enter 'married' or 'single'.")

def survey():
    questions = [
        ("What is your name? ", get_nonempty),
        ("How old are you? ", get_valid_age),
        ("What is your favorite color? ", get_nonempty),
        ("Where were you born? ", get_nonempty),
        ("What is your favorite food? ", get_nonempty),
        ("What is your favorite hobby? ", get_nonempty),
        ("Are you married or single?", get_status)
    ]
    all_responses = []
    while True:
        print("\nNew Survey Participant (or type 'q' to quit):")
        responses = []
        for question, validator in questions:
            answer = validator(question)
            if answer.lower() == 'q':
                return all_responses
            responses.append(answer)
        all_responses.append(responses)
        cont = input("Add another participant? (y/n): ")
        if cont.lower() != 'y':
            break
    return all_responses

def view_results(questions, all_responses):
    if not all_responses:
        print("No survey results yet.")
        return
    for idx, responses in enumerate(all_responses, 1):
        print(f"\nParticipant {idx}:")
        for q, a in zip(questions, responses):
            print(f"{q} {a}")

def main():
    questions = [
        "What is your name? ",
        "How old are you? ",
        "What is your favorite color? ",
        "Where were you born? ",
        "What is your favorite food? ",
        "What is your favorite hobby? ",
        "Are you married or single? "
    ]
    all_responses = []
    while True:
        print("\nSurvey Menu:")
        print("1. Take Survey")
        print("2. View Results")
        print("3. Analyze Data")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            while True:
                if not survey(questions, all_responses):
                    break
                cont = input("Add another participant? (y/n): ")
                if cont.lower() != "y":
                    break
        elif choice == "2":
            view_results(questions, all_responses)
        elif choice == "3":
            print("\nAnalysis:")
            average_age(all_responses)
            most_common_color(all_responses)
            marital_status_count(all_responses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()
