"""Seed script: populates the database with 30 products and ~200 orders/returns."""

import sys
import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Product, SizeChart, UserMeasurement, Order, Return

fake = Faker()
random.seed(42)

# Size chart templates (chest, waist, hip in cm) per standard sizing
SIZE_TEMPLATES = {
    "XS": {"chest": 82, "waist": 62, "hip": 88},
    "S": {"chest": 88, "waist": 68, "hip": 94},
    "M": {"chest": 94, "waist": 74, "hip": 100},
    "L": {"chest": 100, "waist": 80, "hip": 106},
    "XL": {"chest": 106, "waist": 86, "hip": 112},
    "XXL": {"chest": 112, "waist": 92, "hip": 118},
}
SIZES = ["XS", "S", "M", "L", "XL", "XXL"]

BRANDS = [
    {"id": 1, "name": "UrbanEdge"},
    {"id": 2, "name": "Stride"},
    {"id": 3, "name": "Lumina"},
    {"id": 4, "name": "Nomad"},
    {"id": 5, "name": "Velour"},
]

CATEGORIES = ["tops", "jeans", "dresses", "jackets", "shorts"]

PRODUCT_TEMPLATES = [
    # tops
    ("Classic White Tee", "tops", 29.99),
    ("Striped Linen Shirt", "tops", 49.99),
    ("Floral Wrap Top", "tops", 39.99),
    ("Ribbed Crop Top", "tops", 24.99),
    ("Oversized Graphic Tee", "tops", 34.99),
    ("Silk Blouse", "tops", 79.99),
    # jeans
    ("Slim Fit Jeans", "jeans", 69.99),
    ("High-Rise Mom Jeans", "jeans", 74.99),
    ("Straight Leg Denim", "jeans", 64.99),
    ("Distressed Skinny Jeans", "jeans", 59.99),
    ("Wide Leg Jeans", "jeans", 79.99),
    ("Cargo Denim", "jeans", 84.99),
    # dresses
    ("Floral Midi Dress", "dresses", 89.99),
    ("Wrap Maxi Dress", "dresses", 99.99),
    ("Mini Slip Dress", "dresses", 59.99),
    ("Shirt Dress", "dresses", 79.99),
    ("Bodycon Dress", "dresses", 69.99),
    ("Boho Sundress", "dresses", 74.99),
    # jackets
    ("Denim Jacket", "jackets", 89.99),
    ("Leather Biker Jacket", "jackets", 149.99),
    ("Quilted Puffer Jacket", "jackets", 129.99),
    ("Trench Coat", "jackets", 159.99),
    ("Windbreaker", "jackets", 79.99),
    ("Wool Blazer", "jackets", 119.99),
    # shorts
    ("Linen Shorts", "shorts", 39.99),
    ("Denim Cut-Offs", "shorts", 44.99),
    ("Sporty Biker Shorts", "shorts", 29.99),
    ("Paperbag Waist Shorts", "shorts", 49.99),
    ("Bermuda Shorts", "shorts", 54.99),
    ("Chino Shorts", "shorts", 44.99),
]

RETURN_REASONS = ["too_small", "too_large", "quality", "other"]
ORDER_STATUSES = ["pending", "shipped", "delivered", "returned"]


def seed_products():
    """Create 30 products with size charts."""
    products = []
    for idx, (name, category, price) in enumerate(PRODUCT_TEMPLATES):
        brand = BRANDS[idx % len(BRANDS)]
        product = Product(
            name=name,
            brand=brand["name"],
            brand_id=brand["id"],
            category=category,
            price=price,
            description=fake.sentence(nb_words=12),
            image_url=f"https://picsum.photos/seed/{idx + 1}/400/300",
            stock=random.randint(50, 200),
        )
        db.session.add(product)
        db.session.flush()  # get product.id

        # Add size chart with slight per-product variation
        variation = random.uniform(-2, 2)
        for size in SIZES:
            tmpl = SIZE_TEMPLATES[size]
            sc = SizeChart(
                product_id=product.id,
                size=size,
                chest=round(tmpl["chest"] + variation, 1),
                waist=round(tmpl["waist"] + variation, 1),
                hip=round(tmpl["hip"] + variation, 1),
            )
            db.session.add(sc)

        products.append(product)

    db.session.commit()
    print(f"  Created {len(products)} products with size charts.")
    return products


def seed_users():
    """Create 1 admin + 49 customer users."""
    users = []

    # Admin user
    admin = User(username="admin", email="admin@fitright.com", role="admin")
    admin.set_password("Admin@1234")
    db.session.add(admin)
    db.session.flush()

    # Add measurements for admin
    m = UserMeasurement(user_id=admin.id, chest=94, waist=78, hip=100)
    db.session.add(m)
    users.append(admin)

    # 49 customers
    for i in range(49):
        username = fake.user_name() + str(i)
        email = fake.unique.email()
        user = User(username=username, email=email, role="customer")
        user.set_password("password123")
        db.session.add(user)
        db.session.flush()

        # Random measurements near standard sizes
        base_size = random.choice(list(SIZE_TEMPLATES.values()))
        m = UserMeasurement(
            user_id=user.id,
            chest=round(base_size["chest"] + random.uniform(-5, 5), 1),
            waist=round(base_size["waist"] + random.uniform(-5, 5), 1),
            hip=round(base_size["hip"] + random.uniform(-5, 5), 1),
        )
        db.session.add(m)
        users.append(user)

    db.session.commit()
    print(f"  Created {len(users)} users (1 admin + {len(users)-1} customers).")
    return users


def seed_orders_returns(users, products):
    """Create ~200 orders with a subset becoming returns."""
    customers = [u for u in users if u.role == "customer"]
    orders_created = 0
    returns_created = 0

    for _ in range(200):
        user = random.choice(customers)
        product = random.choice(products)
        size = random.choice(SIZES)
        status = random.choice(ORDER_STATUSES)
        created_at = datetime.utcnow() - timedelta(days=random.randint(1, 180))

        order = Order(
            user_id=user.id,
            product_id=product.id,
            size=size,
            status=status,
            created_at=created_at,
        )
        db.session.add(order)
        db.session.flush()
        orders_created += 1

        # If returned, add a return record
        if status == "returned":
            reason = random.choice(RETURN_REASONS)
            ret = Return(
                order_id=order.id,
                reason=reason,
                note=fake.sentence(nb_words=8) if random.random() > 0.4 else None,
                created_at=created_at + timedelta(days=random.randint(1, 14)),
            )
            db.session.add(ret)
            returns_created += 1

    db.session.commit()
    print(f"  Created {orders_created} orders, {returns_created} returns.")


def main():
    app = create_app("development")
    with app.app_context():
        print("Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()

        print("Seeding products...")
        products = seed_products()

        print("Seeding users...")
        users = seed_users()

        print("Seeding orders and returns...")
        seed_orders_returns(users, products)

        print("\nSeed complete!")
        print("  Admin login: admin@fitright.com / Admin@1234")


if __name__ == "__main__":
    main()
