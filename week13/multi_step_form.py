from flask import Flask, session, redirect, url_for, render_template, request, flash

app = Flask(__name__, template_folder='multi_templates')
app.secret_key = "dev-secret-change"

STEPS = [
	{
		"title": "Step 1: Personal Info",
		"fields": [
			{"name": "first_name", "label": "First Name", "required": True},
			{"name": "last_name", "label": "Last Name", "required": True},
		],
	},
	{
		"title": "Step 2: Contact",
		"fields": [
			{"name": "email", "label": "Email", "required": True},
			{"name": "phone", "label": "Phone", "required": False},
		],
	},
	{
		"title": "Step 3: Address",
		"fields": [
			{"name": "city", "label": "City", "required": True},
			{"name": "state", "label": "State", "required": True},
		],
	},
]

def get_data():
	return session.get("form_data", {})

def save_data(d):
	session["form_data"] = d

@app.route("/")
def home():
	return redirect(url_for("start"))

@app.route("/start")
def start():
	# Reset progress start
	session["current_step"] = 0
	session["form_data"] = {}
	return redirect(url_for("step", n=1))

@app.route("/step/<int:n>", methods=["GET", "POST"])
def step(n: int):
	if n < 1 or n > len(STEPS):
		flash("Invalid step.")
		return redirect(url_for("start"))
	idx = n - 1
	step_def = STEPS[idx]
	data = get_data()

	if request.method == "POST":
		# Handle navigation buttons
		if "prev" in request.form:
			return redirect(url_for("step", n=n-1 if n > 1 else 1))
		if "cancel" in request.form:
			return redirect(url_for("reset"))

		# Collect and validate fields
		errors = []
		for f in step_def["fields"]:
			val = request.form.get(f["name"], "").strip()
			if f.get("required") and not val:
				errors.append(f"{f['label']} is required.")
			else:
				data[f["name"]] = val
		if errors:
			for e in errors:
				flash(e)
		else:
			save_data(data)
			if n == len(STEPS):
				return redirect(url_for("summary"))
			return redirect(url_for("step", n=n+1))

	# GET render
	filled = {f["name"]: get_data().get(f["name"], "") for f in step_def["fields"]}
	return render_template("step.html", step=step_def, n=n, total=len(STEPS), values=filled)

@app.route("/summary", methods=["GET", "POST"])
def summary():
	data = get_data()
	if request.method == "POST":
		if "confirm" in request.form:
			flash("Submitted!")
			return redirect(url_for("reset"))
		if "back" in request.form:
			return redirect(url_for("step", n=len(STEPS)))
	return render_template("summary.html", data=data)

@app.route("/reset")
def reset():
	session.pop("form_data", None)
	session.pop("current_step", None)
	flash("Form reset.")
	return redirect(url_for("start"))

if __name__ == "__main__":
	app.run(debug=True)
