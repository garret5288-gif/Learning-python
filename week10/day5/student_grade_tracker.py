from flask import Flask, render_template, request, redirect, url_for
import json
import os
# Initialize the in-memory student data
app = Flask(__name__, template_folder="tracker_templates", static_folder="tracker_templates")

# Persist within the templates/static folder so it's easy to edit alongside the UI assets
DATA_FILE = os.path.join(os.path.dirname(__file__), 'tracker_templates', 'students.json')

STUDENTS = [] # In-memory list of student records

def add_student(name: str, math: list, science: list, english: list): # Add a new student and save to file
    STUDENTS.append({"name": name, "math": math, "science": science, "english": english})
    save_data()
    return STUDENTS

def save_data(): # Save student data to JSON file
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(STUDENTS, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_data(): # Load student data from JSON file
    global STUDENTS
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                STUDENTS = json.load(f)
        except Exception:
            # Ignore and keep current in-memory defaults
            pass




@app.route('/') # Home page
def home():
    return render_template("home.html")


@app.route('/students') # Students list page
def students_page():
    return render_template("students.html", students=STUDENTS)

@app.route('/grades') # Grades summary page
def grades_page():
    # Compute class averages across all grades entered for each course
    def flatten_and_avg(items, key): # Flatten lists and compute average
        vals = [] # Collect all grades
        for s in items:
            vals.extend(s.get(key, []) or [])
        return (sum(vals) / len(vals)) if vals else 0

    avg_math = flatten_and_avg(STUDENTS, 'math')
    avg_science = flatten_and_avg(STUDENTS, 'science')
    avg_english = flatten_and_avg(STUDENTS, 'english')
    avg_overall = (avg_math + avg_science + avg_english) / 3 if (avg_math or avg_science or avg_english) else 0

    class_avg = { # Summary of class averages
        'math': avg_math,
        'science': avg_science,
        'english': avg_english,
        'overall': avg_overall,
    }
    return render_template("grades.html", students=STUDENTS, class_avg=class_avg)

@app.route('/add', methods=['GET', 'POST']) # Add student page
def add_page():
    error = None # Initialize error message
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        math_raw = (request.form.get('math') or '').strip()
        science_raw = (request.form.get('science') or '').strip()
        english_raw = (request.form.get('english') or '').strip()

        def parse_list(raw): # Parse comma-separated grades into list of integers
            if not raw:
                return []
            parts = [p.strip() for p in raw.split(',')] # Split and strip
            vals = []
            for p in parts: # Iterate parts
                if p == '':
                    continue
                vals.append(int(p)) # Convert to integer
            return vals

        try: # Parse grades
            math_list = parse_list(math_raw)
            science_list = parse_list(science_raw)
            english_list = parse_list(english_raw)
        except ValueError:
            error = "Grades must be integers separated by commas (e.g., 90, 85, 100)."
        else: # Validate and add student
            if not name:
                error = "Name is required."
            elif any(g < 0 or g > 100 for g in math_list + science_list + english_list):
                error = "Grades must be between 0 and 100."
            else: # Add student
                add_student(name, math_list, science_list, english_list)
                return redirect(url_for('students_page'))
    return render_template('add.html', error=error)

if __name__ == '__main__':
    load_data()
    app.run(debug=True)