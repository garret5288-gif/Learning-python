from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__, template_folder="blog_templates", static_folder="blog_templates/static")

posts = [
    {
        "title": "My First Blog Post",
        "author": "Garret",
        "date": "2025-01-15",
        "content": "This is the content of my first blog post. I'm excited to start blogging!"
    },
    {
        "title": "A Day in the Life",
        "author": "Garret",
        "date": "2025-02-10",
        "content": "Today, I want to share what a typical day looks like for me."
    },
    {
        "title": "Exploring Python",
        "author": "Garret",
        "date": "2025-03-05",
        "content": "Python is such a versatile language. Here are some cool things I've learned."
    }
]

@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
