# app/routes/inventory.py (or dashboard.py)
from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask import Blueprint, render_template
from functools import wraps
from flask import session, g
from app.models.products import Product # Import the Product model
from app.models.User import User
from app.models.Business import Business


inventory_bp = Blueprint('inventory', __name__) # Or dashboard_bp

# A simple decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session: # Check if 'user' is in session
            flash('Please log in to access this page.', 'warning') # Flash a message
            return redirect(url_for('auth.login')) # Redirect to login page
        return f(*args, **kwargs) # If logged in, proceed to the function
    return wrapper

# We need a function to get the current user and business
@inventory_bp.before_request
def get_user_and_business():
    user_id = session.get('user')
    g.user = User.query.get(user_id) if user_id else None
    if g.user:
        g.business = g.user.business
    else:
        g.business = None


@inventory_bp.route('/dashboard')
@login_required
def view_dashboard():
    # Check if business exists (additional safety check)
    if not g.business:
        flash('Business information not found. Please contact support.', 'error')
        return redirect(url_for('auth.login'))
    
    # Fetch all products for the logged-in business
    products = Product.query.filter_by(business_id=g.business.id).all()
    return render_template('dashboard.html', products=products)

@inventory_bp.route('/products')
@login_required
def view_products():
    # Fetch all products for the logged-in business
    products = Product.query.filter_by(business_id=g.business.id).all()
    return render_template('products.html', products=products)

