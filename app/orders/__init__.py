from flask import Blueprint

orders = Blueprint('orders', __name__, template_folder='templates')

from app.orders import routes  # noqa: F401, E402
