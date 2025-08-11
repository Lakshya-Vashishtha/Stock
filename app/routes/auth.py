# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
# Import forms from the new forms.py file
from app.routes.forms import RegistrationForm, LoginForm 
from app.models import User, Business # Import both User and Business models
from app import db # Assuming your SQLAlchemy database instance is named 'db' and initialized in app/__init__.py

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """
    Redirects the root URL to the login page.
    """
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    If the user is already logged in, redirects them to the task view.
    Otherwise, processes the registration form, creating a User and a Business.
    """
    # Check if the user is already logged in
    if 'user' in session:
        flash('You are already logged in!', 'info')
        # Redirect to the dashboard
        return redirect(url_for('inventory.dashboard'))
    
    # Initialize the registration form
    form = RegistrationForm()

    # Process form submission
    if form.validate_on_submit():
        shop_name = form.shop_name.data
        email = form.email.data
        password = form.password.data

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please use a different email or log in.", "error")
            return redirect(url_for('auth.register'))
        
        # Check if shop name already exists
        existing_business = Business.query.filter_by(shop_name=shop_name).first()
        if existing_business:
            flash("Shop name already taken. Please choose a different name.", "error")
            return redirect(url_for('auth.register'))

        try:
            # Create a new Business instance
            new_business = Business(shop_name=shop_name)
            db.session.add(new_business)
            db.session.flush() # Flush to get the new_business.id before committing

            # Create a new User instance and link it to the business
            new_user = User(email=email, business_id=new_business.id)
            new_user.set_password(password) # This method should hash the password
            
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Your shop is set up. You can now log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback() # Rollback in case of any error during the process
            flash(f"An error occurred during registration: {e}", "error")
            print(f"Registration error: {e}") # Log the error for debugging
            return redirect(url_for('auth.register'))

    # Render the registration template with the form
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    Processes the login form and authenticates the user using email.
    """
    # Improvement: Check if the user is already logged in
    if 'user' in session:
        flash('You are already logged in!', 'info')
        return redirect(url_for('inventory.view_dashboard'))

    # Initialize the login form
    form = LoginForm()
    
    # Process form submission
    if form.validate_on_submit():
        # Query the User model by email, which is the login identifier
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and the password is correct
        if user and user.check_password(form.password.data):
            # Store user ID in session upon successful login
            print(user)
            session['user'] = user.id
            flash('Login successful! Welcome back.', 'success')
            # Redirect to the dashboard
            return redirect(url_for('inventory.view_dashboard'))
        
        # Flash an error message for invalid credentials
        flash('Invalid email or password. Please try again.', 'error')
    
    # Render the login template with the form
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """
    Logs out the current user by removing their ID from the session.
    """
    # Remove 'user' from the session
    session.pop('user', None)
    flash('Logged out successfully! See you next time.', 'warning')
    # Redirect to the login page
    return redirect(url_for('auth.login'))
