import csv
import os

def menu():
    print("Survey Menu")
    print("1. Take Survey")
    print("2. View Results")
    print("3. Clear Results")
    print("4. Analyze Data")
    print("5. Exit")

def survey_questions():
    questions = [
        "What is your name?",
        "How old are you?",
        "What is your gender?",
        "What is your favorite color?",
        "What is your favorite food?",]
    responses = {}
    for q in questions:
        ans = input(q + " ")
        responses[q] = ans
    return responses

def save_survey(responses):
    with open("survey_results.csv", "a") as file:
        for q, a in responses.items():
            file.write(f"{q},{a}\n")
        file.write("\n")  # Separate entries
    print("Survey saved.\n")

def view_results():
    try:
        with open("survey_results.csv", "r") as file:
            entries = file.read()
            if not entries.strip():
                print("No survey results found.\n")
                return
            print("\nSurvey Results:\n")
            print(entries)
    except FileNotFoundError:
        print("No survey results found.\n")

def clear_results():
    with open("survey_results.csv", "w") as file:
        pass  # Just open and close to clear the file
    print("All survey results cleared.\n")

def analyze_data():
    try:
        with open("survey_results.csv", "r") as file:
            lines = file.readlines()
            if not lines or all(not line.strip() for line in lines):
                print("No data to analyze.\n")
                return
            age_sum = 0
            age_count = 0
            color_count = {}
            food_count = {}
            for line in lines:
                if line.strip():
                    q, a = line.strip().split(",", 1)
                    if q == "How old are you?":
                        try:
                            age_sum += int(a)
                            age_count += 1
                        except ValueError:
                            pass
                    elif q == "What is your favorite color?":
                        color_count[a] = color_count.get(a, 0) + 1
                    elif q == "What is your favorite food?":
                        food_count[a] = food_count.get(a, 0) + 1
            if age_count > 0:
                avg_age = age_sum / age_count
                print(f"Average Age: {avg_age:.2f}")
            else:
                print("No age data available.")
            if color_count:
                fav_color = max(color_count, key=color_count.get)
                print(f"Most Popular Color: {fav_color} ({color_count[fav_color]} votes)")
            else:
                print("No color data available.")
            if food_count:
                fav_food = max(food_count, key=food_count.get)
                print(f"Most Popular Food: {fav_food} ({food_count[fav_food]} votes)")
            else:
                print("No food data available.")
            print()
    except FileNotFoundError:
        print("No data to analyze.\n")

def main():
    while True:
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            responses = survey_questions()
            save_survey(responses)
        elif choice == "2":
            view_results()
        elif choice == "3":
            clear_results()
        elif choice == "4":
            analyze_data()
        elif choice == "5":
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()