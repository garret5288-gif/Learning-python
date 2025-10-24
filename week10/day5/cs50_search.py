from flask import Flask, render_template

# Configure Flask to load templates and static assets from the cs50_templates folder
app = Flask(__name__,template_folder="cs50_templates",static_folder="cs50_templates",)


@app.route("/")
def home():
	return render_template("base.html")


@app.route("/images")
def images():
	return render_template("images.html")


@app.route("/advanced")
def advanced():
	return render_template("advanced.html")


if __name__ == "__main__":
	app.run(debug=True)
