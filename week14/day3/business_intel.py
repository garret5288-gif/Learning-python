from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
import csv, io, json, random

app = Flask(__name__, template_folder="bi_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///business_intel.db'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
db = SQLAlchemy(app)

class Dataset(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class DatasetRow(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
	data = db.Column(db.Text, nullable=False)  # JSON blob
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	dataset = db.relationship('Dataset', backref=db.backref('rows', lazy='dynamic'))

class KPI(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	expression = db.Column(db.String(255), nullable=False)  # simple formula referencing columns SUM(sales_amount)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

def ensure_schema():
	with app.app_context():
		db.create_all()

def parse_row(row: DatasetRow):
	try:
		return json.loads(row.data)
	except Exception:
		return {}

# ---- Ingestion ----
def ingest_csv(file_storage, name: str):
	content = file_storage.read().decode('utf-8', errors='ignore')
	reader = csv.DictReader(io.StringIO(content))
	ds = Dataset(name=name)
	db.session.add(ds)
	db.session.flush()
	for r in reader:
		db.session.add(DatasetRow(dataset_id=ds.id, data=json.dumps(r)))
	db.session.commit()
	return ds

def generate_sample(name: str, days: int = 14, daily_orders: int = 30):
	ds = Dataset(name=name)
	db.session.add(ds)
	db.session.flush()
	base_date = datetime.utcnow().date() - timedelta(days=days-1)
	for d in range(days):
		day = base_date + timedelta(days=d)
		for _ in range(daily_orders):
			order_id = f"O{day.strftime('%Y%m%d')}-{random.randint(1000,9999)}"
			qty = random.randint(1,5)
			price = random.choice([9.99, 14.99, 24.99, 49.00])
			row = {
				'date': day.isoformat(),
				'order_id': order_id,
				'product': random.choice(['Widget','Gadget','Premium','Addon']),
				'qty': qty,
				'unit_price': price,
				'sales_amount': round(qty * price, 2)
			}
			db.session.add(DatasetRow(dataset_id=ds.id, data=json.dumps(row)))
	db.session.commit()
	return ds

# ---- Analytics helpers ----
def daily_aggregate(rows: list[dict]):
	agg = {}
	for r in rows:
		day = r.get('date') or r.get('timestamp')
		if not day:
			continue
		sales = float(r.get('sales_amount') or (r.get('qty') or 0) * (r.get('unit_price') or 0))
		agg.setdefault(day, {'sales':0.0,'orders':0,'qty':0})
		agg[day]['sales'] += sales
		agg[day]['orders'] += 1
		agg[day]['qty'] += float(r.get('qty') or 0)
	# finalize avg order value
	out = []
	for day, v in sorted(agg.items()):
		avg_order_value = v['sales']/v['orders'] if v['orders'] else 0
		out.append({'day': day, 'sales': round(v['sales'],2), 'orders': v['orders'], 'avg_order_value': round(avg_order_value,2)})
	return out

def kpi_value(kpi: KPI, rows: list[dict]):
	expr = kpi.expression.strip().upper()
	if expr.startswith('SUM(') and expr.endswith(')'):
		col = expr[4:-1].lower()
		total = 0.0
		for r in rows:
			v = r.get(col)
			try:
				total += float(v)
			except Exception:
				pass
		return round(total,2)
	if expr == 'COUNT':
		return len(rows)
	return None

# ---- Routes ----
@app.route('/', methods=['GET','POST'])
def dashboard():
	ensure_schema()
	if request.method == 'POST':
		mode = request.form.get('mode')
		name = (request.form.get('name') or '').strip() or f"Dataset {datetime.utcnow().isoformat()}"
		if mode == 'csv' and 'csv_file' in request.files:
			f = request.files['csv_file']
			if f and f.filename:
				ingest_csv(f, name)
		elif mode == 'sample':
			generate_sample(name)
		elif mode == 'kpi':
			kpi_name = (request.form.get('kpi_name') or '').strip()
			expr = (request.form.get('expression') or '').strip()
			if kpi_name and expr:
				db.session.add(KPI(name=kpi_name, expression=expr))
				db.session.commit()
		return redirect(url_for('dashboard'))
	datasets = Dataset.query.order_by(Dataset.created_at.desc()).all()
	kpis = KPI.query.order_by(KPI.created_at.desc()).all()
	# For each dataset compute latest 7 days sales spark
	ds_summaries = []
	for ds in datasets[:6]:
		rows = [parse_row(r) for r in ds.rows.limit(2000).all()]
		daily = daily_aggregate(rows)[-7:]
		total_sales = sum(d['sales'] for d in daily)
		ds_summaries.append({'dataset': ds, 'daily': daily, 'total_sales': round(total_sales,2)})
	# KPI values over all rows (simple)
	all_rows = [parse_row(r) for r in DatasetRow.query.limit(5000).all()]
	kpi_values = {k.id: kpi_value(k, all_rows) for k in kpis}
	return render_template('dashboard.html', ds_summaries=ds_summaries, kpis=kpis, kpi_values=kpi_values)

@app.route('/dataset/<int:dataset_id>')
def dataset_view(dataset_id):
	ensure_schema()
	ds = Dataset.query.get_or_404(dataset_id)
	rows = [parse_row(r) for r in ds.rows.limit(5000).all()]
	daily = daily_aggregate(rows)
	return render_template('dataset.html', dataset=ds, rows=rows[:200], daily=daily[-30:])

@app.route('/api/dataset/<int:dataset_id>/daily')
def api_dataset_daily(dataset_id):
	ensure_schema()
	ds = Dataset.query.get_or_404(dataset_id)
	rows = [parse_row(r) for r in ds.rows.limit(10000).all()]
	return jsonify(daily_aggregate(rows))

@app.route('/api/kpis')
def api_kpis():
	ensure_schema()
	kpis = KPI.query.all()
	all_rows = [parse_row(r) for r in DatasetRow.query.limit(5000).all()]
	return jsonify([{ 'id': k.id, 'name': k.name, 'expression': k.expression, 'value': kpi_value(k, all_rows) } for k in kpis])

if __name__ == '__main__':
	ensure_schema()
	app.run(debug=True, port=5006)