from flask import Flask, render_template
from datetime import datetime

# Serve static assets (css/images) from the templates folder for this simple setup
# This lets {{ url_for('static', filename='...') }} resolve to files under templates/
app = Flask(__name__, static_folder="templates")

@app.route("/")
@app.route("/home")
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template("home.html", current_time=current_time)

@app.route("/about")
def about():
    return render_template("personal.html")


@app.route("/recipe")
def recipe():
    return render_template("recipe.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact")
def contact():
    return render_template("contact_form.html")

if __name__ == "__main__":
    app.run(debug=True)
