from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import csv, io, json

app = Flask(__name__, template_folder="research_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research.db'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
db = SQLAlchemy(app)

class Study(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class DataPoint(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	study_id = db.Column(db.Integer, db.ForeignKey('study.id'), nullable=False)
	participant = db.Column(db.String(100))
	data = db.Column(db.Text, nullable=False)  # JSON blob
	ts = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
	study = db.relationship('Study', backref=db.backref('points', lazy='dynamic'))

def ensure_schema():
	with app.app_context():
		db.create_all()

def parse_point(p: DataPoint):
	try:
		return json.loads(p.data)
	except Exception:
		return {}

def study_stats(study: Study):
	rows = study.points.all()
	count = len(rows)
	participants = set([r.participant for r in rows if r.participant])
	dates = sorted([r.ts.date() for r in rows])
	date_range = (dates[0].isoformat(), dates[-1].isoformat()) if dates else (None, None)
	return {
		'count': count,
		'participants': len(participants),
		'date_range': date_range,
	}

def ingest_csv(study: Study, file_storage):
	content = file_storage.read().decode('utf-8', errors='ignore')
	reader = csv.DictReader(io.StringIO(content))
	for r in reader:
		participant = r.get('participant') or r.get('subject') or None
		db.session.add(DataPoint(study_id=study.id, participant=participant, data=json.dumps(r)))
	db.session.commit()

@app.context_processor
def inject_now():
	return {'now': lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

# ---- Routes ----
@app.route('/', methods=['GET','POST'])
def index():
	ensure_schema()
	if request.method == 'POST':
		title = (request.form.get('title') or '').strip()
		desc = (request.form.get('description') or '').strip() or None
		if title:
			s = Study(title=title, description=desc)
			db.session.add(s)
			db.session.commit()
		return redirect(url_for('index'))
	studies = Study.query.order_by(Study.created_at.desc()).all()
	stats = {s.id: study_stats(s) for s in studies}
	return render_template('index.html', studies=studies, stats=stats)

@app.route('/study/<int:study_id>', methods=['GET','POST'])
def study_view(study_id):
	ensure_schema()
	s = Study.query.get_or_404(study_id)
	if request.method == 'POST':
		mode = request.form.get('mode')
		if mode == 'add_point':
			participant = (request.form.get('participant') or '').strip() or None
			raw_json = (request.form.get('payload') or '').strip()
			payload = {}
			if raw_json:
				try:
					payload = json.loads(raw_json)
				except Exception:
					payload = {'raw': raw_json}
			db.session.add(DataPoint(study_id=s.id, participant=participant, data=json.dumps(payload)))
			db.session.commit()
		elif mode == 'upload_csv' and 'csv_file' in request.files:
			f = request.files['csv_file']
			if f and f.filename:
				ingest_csv(s, f)
		return redirect(url_for('study_view', study_id=s.id))
	points = s.points.order_by(DataPoint.ts.desc()).limit(300).all()
	parsed = [parse_point(p) for p in points]
	stats = study_stats(s)
	return render_template('study.html', study=s, points=points, parsed=parsed, stats=stats)

@app.route('/export/<int:study_id>.json')
def export_json(study_id):
	ensure_schema()
	s = Study.query.get_or_404(study_id)
	rows = [
		{
			'id': p.id,
			'participant': p.participant,
			'ts': p.ts.isoformat(),
			'data': parse_point(p)
		} for p in s.points.order_by(DataPoint.id.asc()).all()
	]
	return jsonify({'study': {'id': s.id, 'title': s.title}, 'points': rows})

@app.route('/api/studies')
def api_studies():
	ensure_schema()
	studies = Study.query.all()
	return jsonify([
		{'id': s.id, 'title': s.title, 'description': s.description, 'stats': study_stats(s)} for s in studies
	])

if __name__ == '__main__':
	ensure_schema()
	app.run(debug=True, port=5007)