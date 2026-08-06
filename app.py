from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import timedelta
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL", "sqlite:///marketplace.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "fallback-secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_seller = db.Column(db.Boolean, default=False)
    shop_name = db.Column(db.String(100), nullable=True)
    area = db.Column(db.String(200), nullable=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    size = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    variants = db.relationship("ProductVariant", backref="product", lazy=True)


class ProductVariant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Welcome to your marketplace!"


@app.route("/buyers/register", methods=["POST"])
def register_buyer():
    data = request.get_json()
    existing = Buyer.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400
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


@app.route("/me")
@jwt_required()
def get_me():
    buyer_id = get_jwt_identity()
    buyer = Buyer.query.get(buyer_id)
    if not buyer:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "id": buyer.id,
        "name": buyer.name,
        "email": buyer.email,
        "is_seller": buyer.is_seller,
        "shop_name": buyer.shop_name,
        "area": buyer.area
    })


@app.route("/become-seller", methods=["POST"])
@jwt_required()
def become_seller():
    buyer_id = get_jwt_identity()
    data = request.get_json()
    buyer = Buyer.query.get(buyer_id)
    if not buyer:
        return jsonify({"message": "User not found"}), 404
    buyer.is_seller = True
    buyer.shop_name = data.get("shop_name")
    buyer.area = data.get("area")
    db.session.commit()
    return jsonify({
        "message": "Seller account activated!",
        "shop_name": buyer.shop_name,
        "area": buyer.area
    })


@app.route("/products/add", methods=["POST"])
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    buyer = Buyer.query.get(user_id)
    if not buyer or not buyer.is_seller:
        return jsonify({"message": "Seller account required"}), 403

    data = request.get_json()
    new_product = Product(
        name=data["name"],
        category=data["category"],
        gender=data["gender"],
        size=data["size"],
        color=data["color"],
        price=data["price"],
        quantity=data["quantity"],
        seller_id=user_id
    )
    db.session.add(new_product)
    db.session.flush()

    variants = data.get("variants", [])
    for variant in variants:
        new_variant = ProductVariant(
            product_id=new_product.id,
            color=variant["color"],
            size=variant["size"],
            quantity=variant["quantity"]
        )
        db.session.add(new_variant)

    db.session.commit()
    return jsonify({"message": "Product added successfully!"})


@app.route("/products")
def get_products():
    products = Product.query.all()
    result = []
    for product in products:
        seller = Buyer.query.get(product.seller_id)
        variants = []
        for v in product.variants:
            variants.append({
                "color": v.color,
                "size": v.size,
                "quantity": v.quantity
            })
        result.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "gender": product.gender,
            "size": product.size,
            "color": product.color,
            "price": product.price,
            "quantity": product.quantity,
            "shop_name": seller.shop_name if seller else "Unknown",
            "variants": variants
        })
    return jsonify(result)


@app.route("/products/search")
def search_products():
    search_term = request.args.get('q')
    color = request.args.get('color')
    size = request.args.get('size')
    category = request.args.get('category')
    gender = request.args.get('gender')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    query = Product.query

    if search_term:
        query = query.filter(Product.name.like(f"%{search_term}%"))
    if color:
        query = query.filter(Product.color.like(f"%{color}%"))
    if size:
        query = query.filter(Product.size.like(f"%{size}%"))
    if category:
        query = query.filter(Product.category == category)
    if gender:
        query = query.filter(Product.gender == gender)
    if min_price:
        query = query.filter(Product.price >= float(min_price))
    if max_price:
        query = query.filter(Product.price <= float(max_price))

    products = query.all()

    if not products:
        return jsonify([])

    result = []
    for product in products:
        seller = Buyer.query.get(product.seller_id)
        variants = []
        for v in product.variants:
            variants.append({
                "color": v.color,
                "size": v.size,
                "quantity": v.quantity
            })
        result.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "gender": product.gender,
            "size": product.size,
            "color": product.color,
            "price": product.price,
            "quantity": product.quantity,
            "shop_name": seller.shop_name if seller else "Unknown",
            "variants": variants
        })
    return jsonify(result)


@app.route("/my-products")
@jwt_required()
def get_my_products():
    seller_id = get_jwt_identity()
    buyer = Buyer.query.get(seller_id)
    if not buyer or not buyer.is_seller:
        return jsonify({"message": "Seller account required"}), 403

    products = Product.query.filter_by(seller_id=seller_id).all()
    result = []
    for product in products:
        variants = []
        for v in product.variants:
            variants.append({
                "color": v.color,
                "size": v.size,
                "quantity": v.quantity
            })
        result.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "gender": product.gender,
            "size": product.size,
            "color": product.color,
            "price": product.price,
            "quantity": product.quantity,
            "variants": variants
        })
    return jsonify(result)


@app.route("/buyers/orders", methods=["POST"])
@jwt_required()
def place_order():
    buyer_id = get_jwt_identity()
    data = request.get_json()

    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"message": "Product not found"}), 404

    selected_size = data.get("size")
    selected_color = data.get("color")
    order_quantity = data["quantity"]

    if product.variants:
        variant = ProductVariant.query.filter_by(
            product_id=product.id,
            size=selected_size,
            color=selected_color
        ).first()

        if not variant:
            return jsonify({"message": "This size/color combination is not available"}), 400

        if variant.quantity < order_quantity:
            return jsonify({"message": f"Only {variant.quantity} available in this size and color"}), 400

        variant.quantity -= order_quantity
    else:
        if product.quantity < order_quantity:
            return jsonify({"message": "Insufficient quantity available"}), 400
        product.quantity -= order_quantity

    new_order = Order(
        buyer_id=buyer_id,
        product_id=data["product_id"],
        quantity=order_quantity,
        size=selected_size,
        color=selected_color
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
            "product_name": product.name if product else "Unknown",
            "quantity": order.quantity,
            "size": order.size,
            "color": order.color,
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
    if str(product.seller_id) != str(seller_id):
        return jsonify({"message": "Not authorized"}), 403
    data = request.get_json()
    order.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Order status updated successfully!"})


@app.route("/sellers/register", methods=["POST"])
def register_seller():
    return jsonify({"message": "Please use /buyers/register and then /become-seller"}), 400


@app.route("/sellers/login", methods=["POST"])
def login_seller():
    data = request.get_json()
    buyer = Buyer.query.filter_by(email=data["email"]).first()
    if buyer and bcrypt.check_password_hash(buyer.password, data["password"]):
        token = create_access_token(identity=str(buyer.id))
        return jsonify({"token": token})
    return jsonify({"message": "Invalid email or password"}), 401

@app.route("/upload-reel", methods=["POST"])
@jwt_required()
def upload_reel():
    user_id = get_jwt_identity()
    buyer = Buyer.query.get(user_id)
    if not buyer or not buyer.is_seller:
        return jsonify({"message": "Seller account required"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files['file']
    
    result = cloudinary.uploader.upload(
        file,
        resource_type="video",
        folder="z-commerce/reels"
    )
    
    return jsonify({
        "url": result["secure_url"],
        "public_id": result["public_id"]
    })


if __name__ == "__main__":
    app.run(debug=False)