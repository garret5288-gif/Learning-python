from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import json, csv, io, statistics

app = Flask(__name__, template_folder="analyzer_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analyzer.db'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB upload limit
db = SQLAlchemy(app)

class Source(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	kind = db.Column(db.String(30), nullable=False)  # 'csv','json','manual'
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class DataRow(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
	data = db.Column(db.Text, nullable=False)  # store JSON string
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	source = db.relationship('Source', backref=db.backref('rows', lazy='dynamic'))

def ensure_schema():
	with app.app_context():
		db.create_all()

# ---- Analysis helpers ----
def parse_row_json(row: DataRow):
	try:
		return json.loads(row.data)
	except Exception:
		return {}

def compute_stats(rows: list[dict]):
	# Determine numeric columns
	numeric_cols = {}
	for r in rows:
		for k, v in r.items():
			if isinstance(v, (int, float)) and not isinstance(v, bool):
				numeric_cols.setdefault(k, []).append(float(v))
	stats = {}
	for col, values in numeric_cols.items():
		if not values:
			continue
		stats[col] = {
			'count': len(values),
			'min': min(values),
			'max': max(values),
			'mean': statistics.fmean(values),
			'median': statistics.median(values),
		}
	return stats

def shared_columns(sources_rows: list[list[dict]]):
	sets = []
	for rows in sources_rows:
		if rows:
			sets.append(set(rows[0].keys()))
	if not sets:
		return []
	return sorted(set.intersection(*sets))

# ---- Ingestion helpers ----
def ingest_csv(file_storage, name: str):
	content = file_storage.read().decode('utf-8', errors='ignore')
	reader = csv.DictReader(io.StringIO(content))
	rows = list(reader)
	src = Source(name=name, kind='csv')
	db.session.add(src)
	db.session.flush()
	for r in rows:
		db.session.add(DataRow(source_id=src.id, data=json.dumps(r)))
	db.session.commit()
	return src

def ingest_json_url(url: str, name: str):
	try:
		import requests
		r = requests.get(url, timeout=6)
		r.raise_for_status()
		data = r.json()
	except Exception:
		data = []
	if isinstance(data, dict):
		data = [data]
	if not isinstance(data, list):
		data = []
	src = Source(name=name, kind='json')
	db.session.add(src)
	db.session.flush()
	for item in data[:500]:
		if isinstance(item, dict):
			db.session.add(DataRow(source_id=src.id, data=json.dumps(item)))
	db.session.commit()
	return src

def ingest_manual(name: str, rows_text: str):
	# Expect JSON lines
	lines = [l.strip() for l in rows_text.splitlines() if l.strip()]
	parsed = []
	for line in lines:
		try:
			obj = json.loads(line)
			if isinstance(obj, dict):
				parsed.append(obj)
		except Exception:
			continue
	src = Source(name=name, kind='manual')
	db.session.add(src)
	db.session.flush()
	for obj in parsed:
		db.session.add(DataRow(source_id=src.id, data=json.dumps(obj)))
	db.session.commit()
	return src

# ---- Routes ----
@app.route('/', methods=['GET', 'POST'])
def index():
	ensure_schema()
	if request.method == 'POST':
		mode = request.form.get('mode')
		name = (request.form.get('name') or '').strip() or f"Source {datetime.utcnow().isoformat()}"
		if mode == 'csv' and 'csv_file' in request.files:
			f = request.files['csv_file']
			if f and f.filename:
				ingest_csv(f, name)
		elif mode == 'json_url':
			url = (request.form.get('json_url') or '').strip()
			if url:
				ingest_json_url(url, name)
		elif mode == 'manual':
			blob = request.form.get('manual_rows') or ''
			ingest_manual(name, blob)
		return redirect(url_for('index'))
	sources = Source.query.order_by(Source.created_at.desc()).all()
	counts = {s.id: s.rows.count() for s in sources}
	return render_template('index.html', sources=sources, counts=counts)

@app.route('/source/<int:source_id>')
def source_detail(source_id):
	ensure_schema()
	src = Source.query.get_or_404(source_id)
	rows = [parse_row_json(r) for r in src.rows.order_by(DataRow.id.asc()).all()]
	stats = compute_stats(rows)
	return render_template('source_detail.html', source=src, rows=rows[:200], stats=stats)

@app.route('/merge')
def merge_view():
	ensure_schema()
	ids = request.args.get('ids', '')
	id_list = [int(i) for i in ids.split(',') if i.isdigit()][:5]
	chosen = Source.query.filter(Source.id.in_(id_list)).all() if id_list else []
	all_rows = [[parse_row_json(r) for r in s.rows.limit(200).all()] for s in chosen]
	merged_stats = [compute_stats(rows) for rows in all_rows]
	common_cols = shared_columns(all_rows)
	return render_template('merge.html', sources=chosen, merged_stats=merged_stats, common_cols=common_cols)

@app.route('/api/source/<int:source_id>/stats')
def api_source_stats(source_id):
	ensure_schema()
	src = Source.query.get_or_404(source_id)
	rows = [parse_row_json(r) for r in src.rows.limit(1000).all()]
	return jsonify({'source_id': src.id, 'stats': compute_stats(rows)})

if __name__ == '__main__':
	ensure_schema()
	app.run(debug=True, port=5004)
