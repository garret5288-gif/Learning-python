from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__, template_folder="inventory_templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
db = SQLAlchemy(app)
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sku = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item,
            'quantity': self.quantity,
            'price': self.price,
            'sku': self.sku,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

def ensure_schema():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/inventory", methods=['GET', 'POST'])
def inventory_page():
    ensure_schema()
    if request.method == 'POST':
        name = (request.form.get('item') or '').strip()
        qty = request.form.get('quantity')
        price = request.form.get('price')
        sku = (request.form.get('sku') or '').strip() or None
        if name and qty is not None and price is not None:
            try:
                iq = int(qty); fp = float(price)
            except Exception:
                iq = None; fp = None
            if iq is not None and fp is not None:
                # Ensure schema and create
                if not (sku and InventoryItem.query.filter(func.lower(InventoryItem.sku) == sku.lower()).first()):
                    item = InventoryItem(item=name, quantity=iq, price=fp, sku=sku)
                    db.session.add(item)
                    db.session.commit()
        # PRG: redirect to avoid form re-submission and ensure a response
        return redirect(url_for('inventory_page'))
    else:
        # Code to view inventory items
        items = InventoryItem.query.order_by(InventoryItem.id.asc()).all()
        return render_template("inventory.html", items=items)
    

# --- API HELPERS ---
def json_error(message, status=400):
    return jsonify({'error': message}), status


# --- PRODUCTS CRUD ---
@app.route('/api/products', methods=['GET'])
def api_products_list():
    ensure_schema()
    q = InventoryItem.query
    # Optional filters: q (search by name or sku), min_qty, max_qty
    query = (request.args.get('q') or '').strip().lower()
    if query:
        q = q.filter(func.lower(InventoryItem.item).like(f'%{query}%') | func.lower(InventoryItem.sku).like(f'%{query}%'))
    try:
        min_qty = int(request.args.get('min_qty') or 0)
        q = q.filter(InventoryItem.quantity >= min_qty)
    except Exception:
        pass
    try:
        max_qty = int(request.args.get('max_qty') or 0)
        if max_qty:
            q = q.filter(InventoryItem.quantity <= max_qty)
    except Exception:
        pass
    q = q.order_by(InventoryItem.id.asc())
    return jsonify([p.to_dict() for p in q.all()])


@app.route('/api/products', methods=['POST'])
def api_products_create():
    ensure_schema()
    data = request.get_json(silent=True) or {}
    name = (data.get('item') or '').strip()
    sku = (data.get('sku') or '').strip() or None
    quantity = data.get('quantity')
    price = data.get('price')
    if not name or quantity is None or price is None:
        return json_error('item, quantity, and price are required.')
    try:
        quantity = int(quantity)
        price = float(price)
    except Exception:
        return json_error('quantity must be int and price must be numeric.')
    if sku and InventoryItem.query.filter(func.lower(InventoryItem.sku) == sku.lower()).first():
        return json_error('SKU already exists.', 409)
    p = InventoryItem(item=name, quantity=quantity, price=price, sku=sku)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route('/api/products/<int:product_id>', methods=['GET'])
def api_products_get(product_id):
    ensure_schema()
    p = InventoryItem.query.get(product_id)
    if not p:
        return json_error('Product not found.', 404)
    return jsonify(p.to_dict())


@app.route('/api/products/<int:product_id>', methods=['PUT', 'PATCH'])
def api_products_update(product_id):
    ensure_schema()
    p = InventoryItem.query.get(product_id)
    if not p:
        return json_error('Product not found.', 404)
    data = request.get_json(silent=True) or {}
    if 'item' in data and (data['item'] or '').strip():
        p.item = data['item'].strip()
    if 'sku' in data:
        new_sku = (data.get('sku') or '').strip() or None
        if new_sku and new_sku != p.sku and InventoryItem.query.filter(func.lower(InventoryItem.sku) == new_sku.lower()).first():
            return json_error('SKU already exists.', 409)
        p.sku = new_sku
    if 'quantity' in data:
        try:
            p.quantity = int(data['quantity'])
        except Exception:
            return json_error('quantity must be int.')
    if 'price' in data:
        try:
            p.price = float(data['price'])
        except Exception:
            return json_error('price must be numeric.')
    p.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(p.to_dict())


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def api_products_delete(product_id):
    ensure_schema()
    p = InventoryItem.query.get(product_id)
    if not p:
        return json_error('Product not found.', 404)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'status': 'deleted'})


@app.route('/api/products/<int:product_id>/adjust', methods=['POST'])
def api_products_adjust(product_id):
    ensure_schema()
    p = InventoryItem.query.get(product_id)
    if not p:
        return json_error('Product not found.', 404)
    data = request.get_json(silent=True) or {}
    delta = data.get('delta')
    try:
        delta = int(delta)
    except Exception:
        return json_error('delta must be int.')
    p.quantity += delta
    p.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(p.to_dict())


if __name__ == '__main__':
    ensure_schema()
    app.run(debug=True)
    
