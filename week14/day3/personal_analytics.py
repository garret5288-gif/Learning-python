from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
import statistics, json

app = Flask(__name__, template_folder="analytics_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personal_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Metric(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False, unique=True)
	unit = db.Column(db.String(40))  # e.g. 'steps', 'hours', 'kg'
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class MetricEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)
	value = db.Column(db.Float, nullable=False)
	ts = db.Column(db.DateTime, default=datetime.utcnow, index=True, nullable=False)
	note = db.Column(db.String(255))

	metric = db.relationship('Metric', backref=db.backref('entries', lazy='dynamic'))

def ensure_schema():
	with app.app_context():
		db.create_all()

# ---- Analytics helpers ----
def metric_stats(entries):
	if not entries:
		return {}
	values = [e.value for e in entries]
	stats = {
		'count': len(values),
		'min': min(values),
		'max': max(values),
		'avg': statistics.fmean(values),
		'median': statistics.median(values),
	}
	# Last 7 days bucketed by date
	now = datetime.utcnow()
	seven_days_ago = now - timedelta(days=6)
	buckets = {}
	for e in entries:
		if e.ts >= seven_days_ago:
			day = e.ts.date().isoformat()
			buckets.setdefault(day, []).append(e.value)
	spark = []
	for i in range(0, 7):
		day = (seven_days_ago + timedelta(days=i)).date().isoformat()
		vals = buckets.get(day, [])
		spark.append({'day': day, 'avg': statistics.fmean(vals) if vals else 0})
	stats['spark'] = spark
	return stats

def metric_trend(entries):
	# Simple trend: compare last 3 avg vs previous 3 avg
	if len(entries) < 2:
		return 'steady'
	ordered = sorted(entries, key=lambda e: e.ts)
	recent = ordered[-3:]
	prev = ordered[-6:-3]
	if not prev:
		return 'new'
	recent_avg = statistics.fmean([e.value for e in recent])
	prev_avg = statistics.fmean([e.value for e in prev])
	if recent_avg > prev_avg * 1.05:
		return 'up'
	if recent_avg < prev_avg * 0.95:
		return 'down'
	return 'steady'

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	ensure_schema()
	if request.method == 'POST':
		mode = request.form.get('mode')
		if mode == 'new_metric':
			name = (request.form.get('name') or '').strip()
			unit = (request.form.get('unit') or '').strip()
			if name:
				if not Metric.query.filter(func.lower(Metric.name) == name.lower()).first():
					db.session.add(Metric(name=name, unit=unit or None))
					db.session.commit()
		elif mode == 'new_entry':
			metric_id = request.form.get('metric_id', type=int)
			value = request.form.get('value', type=float)
			note = (request.form.get('note') or '').strip() or None
			if metric_id and value is not None:
				m = Metric.query.get(metric_id)
				if m:
					db.session.add(MetricEntry(metric_id=m.id, value=value, note=note))
					db.session.commit()
		return redirect(url_for('dashboard'))
	metrics = Metric.query.order_by(Metric.created_at.asc()).all()
	summaries = []
	for m in metrics:
		entries = m.entries.order_by(MetricEntry.ts.asc()).all()
		stats = metric_stats(entries)
		trend = metric_trend(entries)
		summaries.append({'metric': m, 'stats': stats, 'trend': trend})
	return render_template('dashboard.html', summaries=summaries)

@app.route('/metric/<int:metric_id>', methods=['GET', 'POST'])
def metric_detail(metric_id):
	ensure_schema()
	m = Metric.query.get_or_404(metric_id)
	if request.method == 'POST':
		value = request.form.get('value', type=float)
		note = (request.form.get('note') or '').strip() or None
		if value is not None:
			db.session.add(MetricEntry(metric_id=m.id, value=value, note=note))
			db.session.commit()
		return redirect(url_for('metric_detail', metric_id=m.id))
	entries = m.entries.order_by(MetricEntry.ts.asc()).all()
	stats = metric_stats(entries)
	return render_template('metric_detail.html', metric=m, entries=entries, stats=stats)

@app.route('/api/metrics')
def api_metrics():
	ensure_schema()
	metrics = Metric.query.all()
	payload = []
	for m in metrics:
		entries = m.entries.order_by(MetricEntry.ts.asc()).all()
		payload.append({
			'id': m.id,
			'name': m.name,
			'unit': m.unit,
			'stats': metric_stats(entries),
			'trend': metric_trend(entries),
		})
	return jsonify(payload)

@app.route('/api/metric/<int:metric_id>/entries')
def api_metric_entries(metric_id):
	ensure_schema()
	m = Metric.query.get_or_404(metric_id)
	entries = m.entries.order_by(MetricEntry.ts.asc()).all()
	return jsonify([
		{'id': e.id, 'value': e.value, 'ts': e.ts.isoformat(), 'note': e.note} for e in entries
	])

if __name__ == '__main__':
	ensure_schema()
	app.run(debug=True, port=5005)