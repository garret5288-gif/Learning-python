"""Student Records API

Endpoints:
    GET    /api/students                  List students
    POST   /api/students                  Create student (first_name, last_name, email)
    GET    /api/students/<id>             Get student (includes grades)
    PATCH  /api/students/<id>             Update fields (first_name, last_name, email)
    DELETE /api/students/<id>             Delete student (grades cascade)
    POST   /api/students/<id>/grades      Add grade (subject, score)
    GET    /api/students/<id>/grades      List grades for student
    GET    /api/grades/<grade_id>         Get single grade
    PATCH  /api/grades/<grade_id>         Update grade (subject, score)
    DELETE /api/grades/<grade_id>         Delete grade

Run:
    python week14/student_records.py

Notes:
    - Uses SQLite file student_records.db in current working directory.
    - Returns ISO-8601 timestamps.
    - Email uniqueness enforced (case-insensitive).
"""

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__, template_folder="students_templates")
app.secret_key = "yetanotherdevsecretchangeme"  # Change this in production
DB_PATH = "sqlite:///student_records.db"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    grades = db.relationship('Grade', backref='student', cascade='all, delete-orphan', lazy=True)

    def to_dict(self, include_grades=False):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }
        if include_grades:
            data['grades'] = [g.to_dict() for g in self.grades]
        return data

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'score': self.score,
            'recorded_at': self.recorded_at.isoformat(),
        }

def ensure_schema():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")


@app.route("/students", methods=['GET', 'POST'])
def students_page():
    if request.method == 'POST':
        first = (request.form.get('first_name') or '').strip()
        last = (request.form.get('last_name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        if first and last and email:
            if not Student.query.filter(func.lower(Student.email) == email).first():
                s = Student(first_name=first, last_name=last, email=email)
                db.session.add(s)
                db.session.commit()
        # Redirect PRG would be ideal, but keep it simple (render below)
    students = Student.query.order_by(Student.id.asc()).all()
    # Try template; fallback JSON list if missing
    try:
        return render_template("students.html", students=students)
    except Exception:
        return jsonify([s.to_dict(include_grades=False) for s in students])


@app.route('/students/<int:student_id>', methods=['GET', 'POST'])
def student_detail(student_id):
    s = Student.query.get(student_id)
    if not s:
        return json_error('Student not found.', 404)
    if request.method == 'POST':
        subject = (request.form.get('subject') or '').strip()
        score = request.form.get('score')
        if subject and score is not None:
            try:
                val = float(score)
            except Exception:
                val = None
            if val is not None:
                g = Grade(student_id=student_id, subject=subject, score=val)
                db.session.add(g)
                db.session.commit()
    return render_template('student_detail.html', student=s, grades=s.grades)


# --- API HELPERS ---
def json_error(message, status=400):
    return jsonify({'error': message}), status


# --- STUDENT CRUD ---
@app.route('/api/students', methods=['GET'])
def api_students_list():
    ensure_schema()
    q = Student.query.order_by(Student.id.asc())
    return jsonify([s.to_dict() for s in q.all()])


@app.route('/api/students', methods=['POST'])
def api_students_create():
    ensure_schema()
    data = request.get_json(silent=True) or {}
    first = (data.get('first_name') or '').strip()
    last = (data.get('last_name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    if not first or not last or not email:
        return json_error('first_name, last_name, and email are required.')
    if Student.query.filter(func.lower(Student.email) == email).first():
        return json_error('Email already exists.', 409)
    s = Student(first_name=first, last_name=last, email=email)
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201


@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_students_get(student_id):
    ensure_schema()
    s = Student.query.get(student_id)
    if not s:
        return json_error('Student not found.', 404)
    return jsonify(s.to_dict(include_grades=True))


@app.route('/api/students/<int:student_id>', methods=['PUT', 'PATCH'])
def api_students_update(student_id):
    ensure_schema()
    s = Student.query.get(student_id)
    if not s:
        return json_error('Student not found.', 404)
    data = request.get_json(silent=True) or {}
    changed = False
    if 'first_name' in data and data['first_name'].strip():
        s.first_name = data['first_name'].strip(); changed = True
    if 'last_name' in data and data['last_name'].strip():
        s.last_name = data['last_name'].strip(); changed = True
    if 'email' in data and data['email'].strip():
        new_email = data['email'].strip().lower()
        if new_email != s.email and Student.query.filter(func.lower(Student.email) == new_email).first():
            return json_error('Email already exists.', 409)
        s.email = new_email; changed = True
    if changed:
        db.session.commit()
    return jsonify(s.to_dict(include_grades=True))


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_students_delete(student_id):
    ensure_schema()
    s = Student.query.get(student_id)
    if not s:
        return json_error('Student not found.', 404)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 200


# --- GRADES CRUD ---
@app.route('/api/students/<int:student_id>/grades', methods=['POST'])
def api_grades_create(student_id):
    ensure_schema()
    s = Student.query.get(student_id)
    if not s:
        return json_error('Student not found.', 404)
    data = request.get_json(silent=True) or {}
    subject = (data.get('subject') or '').strip()
    score = data.get('score')
    if not subject or score is None:
        return json_error('subject and score are required.')
    try:
        score = float(score)
    except Exception:
        return json_error('score must be numeric.')
    g = Grade(student_id=student_id, subject=subject, score=score)
    db.session.add(g)
    db.session.commit()
    return jsonify(g.to_dict()), 201


@app.route('/api/students/<int:student_id>/grades', methods=['GET'])
def api_grades_list(student_id):
    ensure_schema()
    s = Student.query.get(student_id)
    if not s:
        return json_error('Student not found.', 404)
    return jsonify([g.to_dict() for g in s.grades])


@app.route('/api/grades/<int:grade_id>', methods=['GET'])
def api_grade_get(grade_id):
    ensure_schema()
    g = Grade.query.get(grade_id)
    if not g:
        return json_error('Grade not found.', 404)
    return jsonify(g.to_dict())


@app.route('/api/grades/<int:grade_id>', methods=['PUT', 'PATCH'])
def api_grade_update(grade_id):
    ensure_schema()
    g = Grade.query.get(grade_id)
    if not g:
        return json_error('Grade not found.', 404)
    data = request.get_json(silent=True) or {}
    if 'subject' in data and data['subject'].strip():
        g.subject = data['subject'].strip()
    if 'score' in data:
        try:
            g.score = float(data['score'])
        except Exception:
            return json_error('score must be numeric.')
    db.session.commit()
    return jsonify(g.to_dict())


@app.route('/api/grades/<int:grade_id>', methods=['DELETE'])
def api_grade_delete(grade_id):
    ensure_schema()
    g = Grade.query.get(grade_id)
    if not g:
        return json_error('Grade not found.', 404)
    db.session.delete(g)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 200


if __name__ == '__main__':
    ensure_schema()
    app.run(debug=True)

