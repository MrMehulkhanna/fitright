from flask import Blueprint

catalog = Blueprint("catalog", __name__, template_folder="templates")

from app.catalog import routes  # noqa: F401, E402
