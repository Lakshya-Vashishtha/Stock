from app import create_app, db
# Import all models here so that `db.create_all()` knows about them.
# The __init__.py in the 'models' directory makes this possible.
from app.models import User, Business, Product

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
