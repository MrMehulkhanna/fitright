"""Pytest fixtures for the FitRight test suite."""
import pytest
from app import create_app, db as _db
from app.models import User, Product, SizeChart, UserMeasurement, Order, Return


@pytest.fixture(scope='session')
def app():
    """Create application with testing config (SQLite in-memory)."""
    _app = create_app('testing')
    with _app.app_context():
        _db.create_all()
        yield _app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Provide a clean DB session for each test, rolled back after."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture(scope='function')
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def sample_product(db):
    """A product with a full size chart."""
    product = Product(
        name='Test Tee',
        brand='TestBrand',
        brand_id=1,
        category='tops',
        price=29.99,
    )
    db.session.add(product)
    db.session.flush()

    size_data = [
        ('XS', 82, 62, 88),
        ('S',  88, 68, 94),
        ('M',  94, 74, 100),
        ('L',  100, 80, 106),
        ('XL', 106, 86, 112),
        ('XXL', 112, 92, 118),
    ]
    for size, chest, waist, hip in size_data:
        sc = SizeChart(
            product_id=product.id,
            size=size,
            chest=chest,
            waist=waist,
            hip=hip,
        )
        db.session.add(sc)

    db.session.commit()
    return product


@pytest.fixture(scope='function')
def customer_user(db):
    """A customer user with measurements."""
    user = User(username='testcustomer', email='customer@test.com', role='customer')
    user.set_password('TestPass@1')
    db.session.add(user)
    db.session.flush()

    m = UserMeasurement(user_id=user.id, chest=94, waist=74, hip=100)
    db.session.add(m)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def admin_user(db):
    """An admin user."""
    user = User(username='testadmin', email='admin@test.com', role='admin')
    user.set_password('AdminPass@1')
    db.session.add(user)
    db.session.commit()
    return user
