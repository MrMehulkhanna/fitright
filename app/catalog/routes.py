"""Catalog blueprint: product listing, detail, and measurement routes."""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.catalog import catalog
from app.catalog.forms import SearchForm, MeasurementForm
from app.models import Product, UserMeasurement
from app.services.recommendation import recommend_size
from app import db

ITEMS_PER_PAGE = 12


@catalog.route('/')
def index():
    """Product listing with search and category filter."""
    form = SearchForm(request.args)
    query = Product.query

    # Apply search filter
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    if q:
        query = query.filter(
            (Product.name.ilike(f'%{q}%')) |
            (Product.brand.ilike(f'%{q}%'))
        )
    if category:
        query = query.filter_by(category=category)

    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Product.category, Product.name).paginate(
        page=page, per_page=ITEMS_PER_PAGE, error_out=False
    )
    products = pagination.items

    return render_template(
        'catalog/index.html',
        products=products,
        pagination=pagination,
        form=form,
        q=q,
        category=category,
        title='Shop - FitRight'
    )


@catalog.route('/products/<int:product_id>')
def product_detail(product_id):
    """Product detail page with optional size recommendation."""
    product = Product.query.get_or_404(product_id)
    size_charts = product.size_charts.order_by('id').all()

    recommendation = None
    if current_user.is_authenticated and current_user.measurements:
        m = current_user.measurements
        recommendation = recommend_size(product_id, m.chest, m.waist, m.hip)

    return render_template(
        'catalog/product.html',
        product=product,
        size_charts=size_charts,
        recommendation=recommendation,
        title=product.name
    )


@catalog.route('/measurements', methods=['GET', 'POST'])
@login_required
def measurements():
    """View and update user body measurements."""
    existing = current_user.measurements
    form = MeasurementForm(obj=existing)

    if form.validate_on_submit():
        if existing:
            existing.chest = form.chest.data
            existing.waist = form.waist.data
            existing.hip = form.hip.data
        else:
            m = UserMeasurement(
                user_id=current_user.id,
                chest=form.chest.data,
                waist=form.waist.data,
                hip=form.hip.data,
            )
            db.session.add(m)
        db.session.commit()
        flash('Measurements saved!', 'success')
        return redirect(url_for('catalog.measurements'))

    return render_template(
        'catalog/measurements.html',
        form=form,
        title='My Measurements'
    )
