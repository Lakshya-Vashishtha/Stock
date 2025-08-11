# app/models/User.py
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # One-to-one relationship with Business
    # A user belongs to one business, and a business has one user
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), unique=True, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        print(self.password_hash)
        print(password)
        return check_password_hash(self.password_hash, password)

    @property
    def username(self):
        return self.full_name or f"User{self.id}"

    def __repr__(self):
        return f"<User {self.full_name}>"