from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
app.config["JWT_SECRET_KEY"] = "your-secret-key-change-this"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shop_name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    products = db.relationship("Product", backref="seller", lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"), nullable=False)

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyer.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    quantity = db.Column(db.Integer, nullable=False)

@app.route("/")
def home():
    return "Welcome to your marketplace!"

@app.route("/sellers/register", methods=["POST"])
def register_seller():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_seller = Seller(
        name=data["name"],
        shop_name=data["shop_name"],
        area=data["area"],
        email=data["email"],
        password=hashed_password
    )
    db.session.add(new_seller)
    db.session.commit()
    return jsonify({"message": "Seller registered successfully!"})

@app.route("/sellers/login", methods=["POST"])
def login_seller():
    data = request.get_json()
    seller = Seller.query.filter_by(email=data["email"]).first()
    if seller and bcrypt.check_password_hash(seller.password, data["password"]):
        token = create_access_token(identity=str(seller.id))
        return jsonify({"token": token})
    return jsonify({"message": "Invalid email or password"}), 401

@app.route("/products/add", methods=["POST"])
@jwt_required()
def add_product():
    seller_id = get_jwt_identity()
    data = request.get_json()
    new_product = Product(
        name=data["name"],
        size=data["size"],
        color=data["color"],
        quantity=data["quantity"],
        seller_id=seller_id
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"})

@app.route("/sellers")
def get_sellers():
    sellers = Seller.query.all()
    result = []
    for seller in sellers:
        result.append({
            "id": seller.id,
            "name": seller.name,
            "shop_name": seller.shop_name,
            "area": seller.area
        })
    return jsonify(result)

@app.route("/sellers/<int:seller_id>/products")
def get_seller_products(seller_id):
    products = Product.query.filter_by(seller_id=seller_id).all()
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "size": product.size,
            "color": product.color,
            "quantity": product.quantity
        })
    return jsonify(result)

@app.route("/buyers/register", methods=["POST"])
def register_buyer():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_buyer = Buyer(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )
    db.session.add(new_buyer)
    db.session.commit()
    return jsonify({"message": "Buyer registered successfully!"})

@app.route("/buyers/login", methods=["POST"])
def login_buyer():
    data = request.get_json()
    buyer = Buyer.query.filter_by(email=data["email"]).first()
    if buyer and bcrypt.check_password_hash(buyer.password, data["password"]):
        token = create_access_token(identity=str(buyer.id))
        return jsonify({"token": token})
    return jsonify({"message": "Invalid email or password"}), 401

@app.route("/buyers/orders", methods=["POST"])
@jwt_required()
def place_order():
    buyer_id = get_jwt_identity()
    data = request.get_json()
    
    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"message": "Product not found"}), 404
    if product.quantity < data["quantity"]:
        return jsonify({"message": "Insufficient quantity available"}), 400
    product.quantity -= data["quantity"]

    new_order = Order(
        buyer_id=buyer_id,
        product_id=data["product_id"],
        quantity=data["quantity"]
    )

    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully!"})


@app.route("/buyers/orders")
@jwt_required()
def get_buyer_orders():
    buyer_id = get_jwt_identity()
    orders = Order.query.filter_by(buyer_id=buyer_id).all()
    result = []
    for order in orders:
        product = Product.query.get(order.product_id)
        result.append({
            "id": order.id,
            "product_name": product.name,
            "quantity": order.quantity,
            "status": order.status
        })
    return jsonify(result)

@app.route("/orders/<int:order_id>/status", methods=["PUT"])
@jwt_required()
def update_order_status(order_id):
    seller_id = get_jwt_identity()
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    product = Product.query.get(order.product_id)
    
    if product.seller_id != int(seller_id):
        return jsonify({"message": "Not authorized to update this order"}), 403
    
    data = request.get_json()
    order.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Order status updated successfully!"})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)