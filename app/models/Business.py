from app.extensions import db

class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(120), unique=True, nullable=False)
    business_type = db.Column(db.String(100), nullable=True) # Made nullable as it's not part of initial registration

    # One-to-one relationship with User
    # 'uselist=False' indicates a one-to-one relationship

    user = db.relationship('User', backref='business', uselist=False, cascade="all, delete-orphan", primaryjoin="Business.id == User.business_id")

    def __repr__(self):
        return f"<Business {self.shop_name}>"