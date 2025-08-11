# app/__init__.py
from flask import Flask
from app.extensions import db
from app.routes.auth import auth_bp
from app.routes.inventory import inventory_bp 
from app.routes.api import api_bp
from flask_migrate import Migrate
from app.models.Business import Business 
from app.models.User import User   
from app.models.products import Product    

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'MYSECRETKEY' # IMPORTANT: Change this to a strong, random key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppresses a warning

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp) 
    app.register_blueprint(api_bp) 

    return app

