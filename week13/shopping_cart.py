from flask import Flask, session, redirect, url_for, render_template, request, flash

app = Flask(__name__, template_folder='shopping_templates')
app.secret_key = 'dev-secret-change'

# In-memory product catalog
PRODUCTS = [
    {"id": "1", "name": "Apple", "price": 0.99},
    {"id": "2", "name": "Banana", "price": 0.59},
    {"id": "3", "name": "Coffee", "price": 3.49},
]

def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart

def find_product(pid):
    for p in PRODUCTS:
        if p['id'] == pid:
            return p
    return None

@app.route('/')
def catalog():
    return render_template('catalog.html', products=PRODUCTS)

@app.route('/add_to_cart/<item_id>', methods=['POST', 'GET'])
def add_to_cart(item_id):
    if not find_product(item_id):
        flash('Item not found.')
        return redirect(url_for('catalog'))
    cart = get_cart()
    cart[item_id] = cart.get(item_id, 0) + 1
    save_cart(cart)
    if request.method == 'POST':
        flash('Added to cart.')
        return redirect(url_for('catalog'))
    return redirect(url_for('view_cart'))

@app.route('/view_cart')
def view_cart():
    cart = get_cart()
    items = []
    total = 0.0
    for pid, qty in cart.items():
        prod = find_product(pid)
        if not prod:
            continue
        line = prod['price'] * qty
        total += line
        items.append({"id": pid, "name": prod['name'], "price": prod['price'], "qty": qty, "line_total": line})
    return render_template('cart.html', items=items, total=total)

@app.route('/remove_from_cart/<item_id>', methods=['POST', 'GET'])
def remove_from_cart(item_id):
    cart = get_cart()
    if item_id in cart:
        if cart[item_id] > 1:
            cart[item_id] -= 1
        else:
            del cart[item_id]
        save_cart(cart)
        flash('Item removed.')
    return redirect(url_for('view_cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared.')
    return redirect(url_for('catalog'))

@app.route('/checkout')
def checkout():
    cart = get_cart()
    items = []
    total = 0.0
    for pid, qty in cart.items():
        prod = find_product(pid)
        if not prod:
            continue
        line = prod['price'] * qty
        total += line
        items.append({"id": pid, "name": prod['name'], "price": prod['price'], "qty": qty, "line_total": line})
    session.pop('cart', None)
    return render_template('checkout.html', items=items, total=total)

if __name__ == '__main__':
    app.run(debug=True)