import csv # for CSV handling
from pathlib import Path # for file paths
from collections import Counter # for counting occurrences

CSV_FILE = Path("survey_results.csv") # path to survey results
HEADER = ["name","age","gender","favorite_color","favorite_food"] # CSV header fields

def menu(): # Display menu options
    print("\nSurvey Menu")
    print("1. Take Survey")
    print("2. View Raw Rows")
    print("3. Clear Results")
    print("4. Analyze Data")
    print("5. Exit")

def ensure_header(): # Ensure CSV has header
    if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:
        with open(CSV_FILE, "w", newline="") as f: # open file for writing
            writer = csv.writer(f)
            writer.writerow(HEADER)

def migrate_legacy_format(): # Convert legacy question,answer blocks into row-based CSV once.
    """Convert legacy question,answer blocks into row-based CSV once."""
    if not CSV_FILE.exists(): # Check if file exists
        return
    # Heuristic: if first line contains a question mark, treat as legacy
    with open(CSV_FILE, "r") as f: # read entire file
        first = f.readline()
        rest = f.read()
    if "?" not in first: # Not legacy format
        return  # already row-based
    blocks = [] # Split into blocks by blank lines
    current = [] # current block of lines
    for line in [first] + rest.splitlines(True): # include first line
        if not line.strip():
            if current: # end of block
                blocks.append(current)
                current = []
            continue
        current.append(line.rstrip("\n"))
    if current: # final block
        blocks.append(current)
    rows = [] # Convert blocks to dict rows
    for blk in blocks:
        data = {k: "" for k in HEADER} # initialize empty row
        for qa in blk: # parse question,answer pairs
            if "," not in qa: # skip malformed lines
                continue
            q, a = qa.split(",",1)
            q = q.strip()
            a = a.strip()
            if q.startswith("What is your name"):
                data["name"] = a
            elif q.startswith("How old are you"):
                data["age"] = a
            elif q.startswith("What is your gender"):
                data["gender"] = a
            elif q.startswith("What is your favorite color"):
                data["favorite_color"] = a
            elif q.startswith("What is your favorite food"):
                data["favorite_food"] = a
        rows.append(data)
    # Overwrite with new format
    with open(CSV_FILE, "w", newline="") as f: # write new CSV
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)

def load_rows(): # Load all rows from CSV
    if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:
        return []
    with open(CSV_FILE, newline="") as f: # open for reading
        reader = csv.DictReader(f)
        return list(reader)

def append_row(row: dict): # Append a single row to CSV
    ensure_header()
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writerow(row)

def clear_results(): # Clear all survey results
    if CSV_FILE.exists():
        CSV_FILE.unlink()
    print("All survey results cleared.\n")

def survey_questions(): # Ask survey questions and return responses as dict
    name = input("Name: ").strip()
    while True: # validate age input
        age_raw = input("Age: ").strip()
        try: # convert to int and check positive
            age = int(age_raw)
            if age <= 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a positive integer for age.")
    gender = input("Gender: ").strip()
    favorite_color = input("Favorite color: ").strip()
    favorite_food = input("Favorite food: ").strip()
    return {"name": name, "age": age, "gender": gender, "favorite_color": favorite_color, "favorite_food": favorite_food}

def view_results(): # View all raw rows
    rows = load_rows()
    if not rows: # No survey results found
        print("No survey results found.\n")
        return
    print("\nRaw Rows:")
    for i, r in enumerate(rows, 1): # display rows with numbering
        print(f"{i}. {r}")
    print()

def analyze_data(): # Analyze survey data
    rows = load_rows()
    if not rows: # No data to analyze
        print("No data to analyze.\n")
        return
    ages = [int(r["age"]) for r in rows if r.get("age") and str(r["age"]).isdigit()] # valid ages
    avg_age = round(sum(ages)/len(ages),2) if ages else 0 # average age
    def most_common(key): # helper to find most common value for a key
        vals = [r[key] for r in rows if r.get(key)] # get values
        if not vals:
            return None, 0
        c = Counter(vals) # count occurrences
        item, count = c.most_common(1)[0]
        return item, count
    gender, gcount = most_common("gender")
    color, ccount = most_common("favorite_color")
    food, fcount = most_common("favorite_food")
    print("\nAnalysis:")
    print(f"Average Age: {avg_age if ages else 'No age data'}")
    print(f"Most Common Gender: {gender} ({gcount})" if gender else "No gender data.")
    print(f"Most Common Color: {color} ({ccount})" if color else "No color data.")
    print(f"Most Common Food: {food} ({fcount})" if food else "No food data.")
    print()

def main(): # Main program loop
    migrate_legacy_format() # convert legacy if needed
    ensure_header() # ensure header exists
    while True:  # Main program loop
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            row = survey_questions()
            append_row(row)
            print("Saved survey.\n")
        elif choice == "2":
            view_results()
        elif choice == "3":
            clear_results()
        elif choice == "4":
            analyze_data()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()