from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, io, csv, json, statistics as stats


app = Flask(__name__, template_folder="file_upload_templates")
app.config['SECRET_KEY'] = 'dev'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB
ALLOWED = {'.csv', '.json', '.txt'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed(filename: str) -> bool:
	_, ext = os.path.splitext(filename.lower())
	return ext in ALLOWED


def process_file(path: str):
	name = os.path.basename(path)
	_, ext = os.path.splitext(name.lower())
	with open(path, 'r', encoding='utf-8', errors='ignore') as f:
		content = f.read()
	result = {"filename": name, "size": os.path.getsize(path), "type": ext or 'unknown'}
	if ext == '.txt':
		lines = content.splitlines()
		words = sum(len(line.split()) for line in lines)
		result.update({"lines": len(lines), "words": words, "preview": content[:400]})
	elif ext == '.json':
		try:
			obj = json.loads(content)
			result.update({"json_type": type(obj).__name__, "keys": list(obj.keys())[:10] if isinstance(obj, dict) else None})
		except Exception as e:
			result.update({"error": f"Invalid JSON: {e}", "preview": content[:400]})
	elif ext == '.csv':
		rows = list(csv.DictReader(io.StringIO(content)))
		result["rows"] = len(rows)
		# simple numeric stats for numeric-looking columns
		numeric_cols = {}
		for row in rows:
			for k, v in row.items():
				if v is None or v == '':
					continue
				try:
					x = float(v)
				except Exception:
					continue
				numeric_cols.setdefault(k, []).append(x)
		col_stats = {}
		for k, values in numeric_cols.items():
			if values:
				col_stats[k] = {
					"count": len(values),
					"min": min(values),
					"max": max(values),
					"avg": sum(values)/len(values),
					"median": stats.median(values),
				}
		result["numeric_stats"] = col_stats
	else:
		result["preview"] = content[:400]
	return result


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part', 'danger')
			return redirect(url_for('index'))
		file = request.files['file']
		if not file or file.filename == '':
			flash('No selected file', 'warning')
			return redirect(url_for('index'))
		if not allowed(file.filename):
			flash('Only .csv, .json, .txt allowed', 'danger')
			return redirect(url_for('index'))
		fname = secure_filename(file.filename)
		save_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
		file.save(save_path)
		result = process_file(save_path)
		return render_template('result.html', result=result)
	return render_template('upload.html')


if __name__ == '__main__':
	app.run(debug=True, port=5008)

