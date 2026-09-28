from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model: customers and admins."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum("customer", "admin"), default="customer", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    measurements = db.relationship(
        "UserMeasurement", backref="user", uselist=False, lazy=True
    )
    orders = db.relationship("Order", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.username}>"


class Product(db.Model):
    """Product catalog."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False, index=True)
    brand_id = db.Column(
        db.Integer, nullable=False, index=True
    )  # brand foreign key placeholder
    category = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    size_charts = db.relationship("SizeChart", backref="product", lazy="dynamic")
    orders = db.relationship("Order", backref="product", lazy="dynamic")

    def __repr__(self):
        return f"<Product {self.name}>"


class SizeChart(db.Model):
    """Size chart entries per product."""

    __tablename__ = "size_charts"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    size = db.Column(db.String(10), nullable=False)  # XS, S, M, L, XL, XXL
    chest = db.Column(db.Float, nullable=False)  # cm
    waist = db.Column(db.Float, nullable=False)  # cm
    hip = db.Column(db.Float, nullable=False)  # cm

    __table_args__ = (
        db.UniqueConstraint("product_id", "size", name="uq_product_size"),
    )

    def __repr__(self):
        return f"<SizeChart {self.product_id} {self.size}>"


class UserMeasurement(db.Model):
    """User body measurements in cm."""

    __tablename__ = "user_measurements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True, index=True
    )
    chest = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    hip = db.Column(db.Float, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<UserMeasurement user={self.user_id}>"


class Order(db.Model):
    """Customer orders."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    size = db.Column(db.String(10), nullable=False)
    status = db.Column(
        db.Enum("pending", "shipped", "delivered", "returned"),
        default="pending",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    returns = db.relationship("Return", backref="order", uselist=False, lazy=True)

    def __repr__(self):
        return f"<Order {self.id} user={self.user_id}>"


class Return(db.Model):
    """Return records linked to orders."""

    __tablename__ = "returns"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True, index=True
    )
    reason = db.Column(
        db.Enum("too_small", "too_large", "quality", "other"), nullable=False
    )
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Return order={self.order_id} reason={self.reason}>"
