# app/models/Product.py
from app.extensions import db

class Product(db.Model):
    """
    Represents a product item in a business's inventory.
    """
    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    stock_level = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.String(10), nullable=True) 

    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"
