from flask import Flask, render_template, abort

app = Flask(__name__, template_folder="product_templates", static_folder="product_templates")
from product_templates.data import products

@app.route('/')
def index():
    return render_template('home.html', products=products)

@app.route('/product/<int:idx>') # Product detail page
def product_page(idx: int):
    if idx < 0 or idx >= len(products):
        abort(404)
    return render_template('product_page.html', product=products[idx])

if __name__ == '__main__':
    app.run(debug=True)    