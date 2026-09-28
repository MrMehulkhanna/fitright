"""Admin blueprint: analytics dashboard with Chart.js visualisations."""
from flask import render_template, abort, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from app.admin import admin
from app.models import Product, Order, Return
from app import db


def _require_admin():
    """Abort with 403 if current user is not an admin."""
    if not current_user.is_authenticated or not current_user.is_admin():
        abort(403)


@admin.route('/')
@login_required
def dashboard():
    """Main admin analytics dashboard."""
    _require_admin()

    # --- Return rate by category ---
    # total orders per category
    total_by_cat = (
        db.session.query(Product.category, func.count(Order.id).label('total'))
        .join(Order, Order.product_id == Product.id)
        .group_by(Product.category)
        .all()
    )
    # returned orders per category
    returned_by_cat = (
        db.session.query(Product.category, func.count(Order.id).label('returned'))
        .join(Order, Order.product_id == Product.id)
        .filter(Order.status == 'returned')
        .group_by(Product.category)
        .all()
    )
    total_map = {row.category: row.total for row in total_by_cat}
    returned_map = {row.category: row.returned for row in returned_by_cat}

    categories = sorted(total_map.keys())
    return_rates = [
        round(returned_map.get(c, 0) / total_map[c] * 100, 1)
        for c in categories
    ]

    # --- Top return reasons ---
    reason_counts = (
        db.session.query(Return.reason, func.count(Return.id).label('cnt'))
        .group_by(Return.reason)
        .all()
    )
    reasons = [r.reason.replace('_', ' ').title() for r in reason_counts]
    reason_values = [r.cnt for r in reason_counts]

    # --- Products with highest size-related returns ---
    size_returns = (
        db.session.query(
            Product.name,
            func.count(Return.id).label('size_returns')
        )
        .join(Order, Order.product_id == Product.id)
        .join(Return, Return.order_id == Order.id)
        .filter(Return.reason.in_(['too_small', 'too_large']))
        .group_by(Product.id, Product.name)
        .order_by(func.count(Return.id).desc())
        .limit(10)
        .all()
    )
    size_return_products = [r.name for r in size_returns]
    size_return_counts = [r.size_returns for r in size_returns]

    # --- Summary KPIs ---
    total_orders = Order.query.count()
    total_returns = Return.query.count()
    overall_return_rate = round(total_returns / total_orders * 100, 1) if total_orders else 0
    total_products = Product.query.count()

    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        # KPIs
        total_orders=total_orders,
        total_returns=total_returns,
        overall_return_rate=overall_return_rate,
        total_products=total_products,
        # Chart data
        categories=categories,
        return_rates=return_rates,
        reasons=reasons,
        reason_values=reason_values,
        size_return_products=size_return_products,
        size_return_counts=size_return_counts,
    )
