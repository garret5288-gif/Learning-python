from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/students')
def students():
    return "Welcome to the Students Page!"

@app.route('/grades')
def grades():
    return "Welcome to the Grades Page!"

if __name__ == '__main__':
    app.run(debug=True)