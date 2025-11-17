from flask import Flask, jsonify, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__, template_folder="personal_templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///personal.db"
db = SQLAlchemy(app)
class PersonalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'created_at': self.created_at.isoformat(),
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    is_done = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_done': self.is_done,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

def ensure_schema():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html') 

@app.route("/records", methods=['GET', 'POST'])
def records_page(): 
    ensure_schema()
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        info = (request.form.get('info') or '').strip()
        if name and info:
            record = PersonalRecord(name=name, info=info)
            db.session.add(record)
            db.session.commit()
        return redirect(url_for('records_page'))
    else:
        records = PersonalRecord.query.order_by(PersonalRecord.id.asc()).all()
        return render_template('records.html', records=records)


# ---- API helpers ----
def json_error(message, status=400):
    return jsonify({'error': message}), status


# ---- Tasks REST API ----
@app.route('/api/tasks', methods=['GET'])
def api_tasks_list():
    ensure_schema()
    q = Task.query
    status = (request.args.get('status') or '').lower()
    if status == 'done':
        q = q.filter(Task.is_done.is_(True))
    elif status == 'open':
        q = q.filter(Task.is_done.is_(False))
    search = (request.args.get('q') or '').strip().lower()
    if search:
        q = q.filter(func.lower(Task.title).like(f'%{search}%') | func.lower(Task.description).like(f'%{search}%'))
    # due_before / due_after (ISO or YYYY-MM-DD)
    def parse_dt(val):
        if not val:
            return None
        try:
            if len(val) == 10:
                return datetime.strptime(val, '%Y-%m-%d')
            return datetime.fromisoformat(val)
        except Exception:
            return None
    due_before = parse_dt(request.args.get('due_before'))
    due_after = parse_dt(request.args.get('due_after'))
    if due_before:
        q = q.filter(Task.due_date <= due_before)
    if due_after:
        q = q.filter(Task.due_date >= due_after)
    sort = (request.args.get('sort') or 'id').lower()
    if sort == 'priority':
        q = q.order_by(Task.priority.desc(), Task.id.asc())
    elif sort == 'due':
        q = q.order_by(Task.due_date.asc().nulls_last(), Task.id.asc())
    else:
        q = q.order_by(Task.id.asc())
    return jsonify([t.to_dict() for t in q.all()])


@app.route('/api/tasks', methods=['POST'])
def api_tasks_create():
    ensure_schema()
    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip() or None
    due = data.get('due_date')
    priority = data.get('priority', 0)
    if not title:
        return json_error('title is required.')
    try:
        priority = int(priority)
    except Exception:
        return json_error('priority must be int.')
    due_dt = None
    if due:
        try:
            due_dt = datetime.fromisoformat(due) if len(due) > 10 else datetime.strptime(due, '%Y-%m-%d')
        except Exception:
            return json_error('due_date must be ISO8601 or YYYY-MM-DD.')
    t = Task(title=title, description=description, due_date=due_dt, priority=priority)
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_tasks_get(task_id):
    ensure_schema()
    t = Task.query.get(task_id)
    if not t:
        return json_error('Task not found.', 404)
    return jsonify(t.to_dict())


@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def api_tasks_update(task_id):
    ensure_schema()
    t = Task.query.get(task_id)
    if not t:
        return json_error('Task not found.', 404)
    data = request.get_json(silent=True) or {}
    if 'title' in data and (data['title'] or '').strip():
        t.title = data['title'].strip()
    if 'description' in data:
        t.description = (data.get('description') or '').strip() or None
    if 'is_done' in data:
        t.is_done = bool(data.get('is_done'))
    if 'priority' in data:
        try:
            t.priority = int(data.get('priority'))
        except Exception:
            return json_error('priority must be int.')
    if 'due_date' in data:
        due = data.get('due_date')
        if due:
            try:
                t.due_date = datetime.fromisoformat(due) if len(due) > 10 else datetime.strptime(due, '%Y-%m-%d')
            except Exception:
                return json_error('due_date must be ISO8601 or YYYY-MM-DD.')
        else:
            t.due_date = None
    t.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(t.to_dict())


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_tasks_delete(task_id):
    ensure_schema()
    t = Task.query.get(task_id)
    if not t:
        return json_error('Task not found.', 404)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'status': 'deleted'})


@app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
def api_tasks_toggle(task_id):
    ensure_schema()
    t = Task.query.get(task_id)
    if not t:
        return json_error('Task not found.', 404)
    t.is_done = not t.is_done
    t.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(t.to_dict())


# ---- Simple Tasks page (optional UI) ----
@app.route('/tasks', methods=['GET', 'POST'])
def tasks_page():
    ensure_schema()
    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        if title:
            t = Task(title=title)
            db.session.add(t)
            db.session.commit()
        return redirect(url_for('tasks_page'))
    tasks = Task.query.order_by(Task.is_done.asc(), Task.priority.desc(), Task.id.asc()).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def tasks_toggle(task_id):
    ensure_schema()
    t = Task.query.get(task_id)
    if t:
        t.is_done = not t.is_done
        t.updated_at = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('tasks_page'))
    
if __name__ == "__main__":
    ensure_schema()
    app.run(debug=True)

