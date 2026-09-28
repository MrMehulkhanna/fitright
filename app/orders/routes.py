"""Orders blueprint: place orders and submit returns."""

from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.orders import orders
from app.orders.forms import OrderForm, ReturnForm
from app.models import Order, Return, Product
from app import db


@orders.route("/")
@login_required
def my_orders():
    """List the current user's orders."""
    user_orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template(
        "orders/my_orders.html", orders=user_orders, title="My Orders"
    )


@orders.route("/place", methods=["POST"])
@login_required
def place_order():
    """Place a new order for a product."""
    form = OrderForm()
    if form.validate_on_submit():
        product = Product.query.get_or_404(int(form.product_id.data))
        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            size=form.size.data,
            status="pending",
        )
        db.session.add(order)
        db.session.commit()
        flash(f"Order placed for {product.name} (Size: {form.size.data}).", "success")
        return redirect(url_for("orders.my_orders"))
    flash("Could not place order. Please try again.", "danger")
    return redirect(request.referrer or url_for("catalog.index"))


@orders.route("/<int:order_id>/return", methods=["GET", "POST"])
@login_required
def return_order(order_id):
    """Submit a return for a delivered order."""
    order = Order.query.get_or_404(order_id)

    # Only the order owner can return it
    if order.user_id != current_user.id:
        abort(403)

    # Only delivered orders can be returned
    if order.status not in ("delivered", "shipped"):
        flash("Only delivered or shipped orders can be returned.", "warning")
        return redirect(url_for("orders.my_orders"))

    # Prevent duplicate returns
    if order.returns:
        flash("This order has already been returned.", "info")
        return redirect(url_for("orders.my_orders"))

    form = ReturnForm()
    if form.validate_on_submit():
        ret = Return(
            order_id=order.id,
            reason=form.reason.data,
            note=form.note.data or None,
        )
        order.status = "returned"
        db.session.add(ret)
        db.session.commit()
        flash("Return submitted successfully.", "success")
        return redirect(url_for("orders.my_orders"))

    return render_template(
        "orders/return_form.html", form=form, order=order, title="Return Order"
    )
