from flask import Flask, render_template

# Look for templates in 'grade_templates' and serve static files (CSS) from there
app = Flask(__name__, template_folder='grade_templates', static_folder='grade_templates')

student_list = [
    {"name": "John Doe", "grades": [85, 90, 78, 92]},
    {"name": "Jane Smith", "grades": [88, 92, 80, 85]},
    {"name": "Emily Johnson", "grades": [90, 85, 95, 88]},
    {"name": "Michael Brown", "grades": [70, 75, 80, 65]},
    {"name": "Jessica Davis", "grades": [95, 100, 98, 97]},
    ]

def calculate_average(grades):
    if not grades:
        return 0
    return sum(grades) / len(grades)

def letter_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/grades')
def grades():
    return render_template('grades.html', students=student_list)

@app.route('/students')
def students():    
    return render_template('students.html', students=student_list)





if __name__ == '__main__':
    app.run(debug=True)
