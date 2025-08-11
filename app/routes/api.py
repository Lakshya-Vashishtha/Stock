# app/routes/api.py
from flask import Blueprint, jsonify, session, g
from app.models.products import Product
from app.models.User import User
from app.models.Business import Business
from app.extensions import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

# We need a function to get the current user and business
@api_bp.before_request
def get_user_and_business():
    user_id = session.get('user')
    g.user = None
    g.business = None
    if user_id:
        g.user = User.query.get(user_id)
        if g.user and g.user.business:
            g.business = g.user.business

@api_bp.route('/dashboard_data')
def dashboard_data():
    if not g.business:
        return jsonify({"error": "Not logged in or business not found"}), 401

    # Fetch all products for this business
    all_products = Product.query.filter_by(business_id=g.business.id).all()
    recent_products = Product.query.filter_by(business_id=g.business.id).order_by(Product.id.desc()).limit(10).all()

    # Compute stats
    total_products = len(all_products)
    low_stock_items = len([p for p in all_products if p.stock_level < 10])

    # --- 🛠️ Calculate dynamic brands & categories ---
    brand_set = set()
    category_set = set()
    for p in all_products:
        if p.brand:
            brand_set.add(p.brand)
        if p.category:
            category_set.add(p.category)

    total_brands = len(brand_set)
    brands_list = sorted(brand_set)
    categories_list = sorted(category_set)

    # Recent products as JSON
    recent_products_json = [{
        'name': p.name,
        'brand': p.brand,
        'category': p.category,
        'stock_level': p.stock_level,
        'price': p.price,
        'expiry_date': p.expiry_date
    } for p in recent_products]

    # Return all data
    data = {
        'shopName': g.business.shop_name,
        'userName': g.user.email,
        'userBusinessType': g.business.business_type or 'General Retail',
        'totalProducts': total_products,
        'salesToday': 0,  # Placeholder
        'monthlySales': 0,  # Placeholder
        'totalBrands': total_brands,
        'lowStockItems': low_stock_items,
        'recentProducts': recent_products_json,
        'salesTrendLabels': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        'salesTrendData': [0, 0, 0, 0, 0, 0, 0],
        'brands': brands_list,
        'categories': categories_list,
        'topProducts': []  # Optional: Can be populated with logic later
    }

    return jsonify(data)
