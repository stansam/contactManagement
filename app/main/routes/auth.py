from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, logout_user, login_user, current_user
from app.models.user import User
from app.main import main_bp
import re

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        flash('You are already registered and logged in.', 'info')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = []

        # Check for empty fields
        if not username:
            errors.append('Username is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if not confirm_password:
            errors.append('Password confirmation is required')

        # Username validation
        if username:
            if len(username) < 3:
                errors.append('Username must be at least 3 characters long')
            if len(username) > 20:
                errors.append('Username must be less than 20 characters')
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                errors.append('Username can only contain letters, numbers, and underscores')

        # Email validation
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors.append('Invalid email format')

        # Password validation
        if password:
            if len(password) < 8:
                errors.append('Password must be at least 8 characters long')
            if not re.search(r'[A-Z]', password):
                errors.append('Password must contain at least one uppercase letter')
            if not re.search(r'[a-z]', password):
                errors.append('Password must contain at least one lowercase letter')
            if not re.search(r'[0-9]', password):
                errors.append('Password must contain at least one number')

        # Password match validation
        if password and confirm_password and password != confirm_password:
            errors.append('Passwords do not match')

        # If there are validation errors, display them
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html', 
                                 username=username, 
                                 email=email)

        # Try to create user
        try:
            user_id = User.create_user(username, email, password)

            if user_id:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('main.login'))
            else:
                flash('Username or email already exists', 'error')
                return render_template('register.html', 
                                     username=username, 
                                     email=email)
        
        except Exception as e:
            flash('An error occurred during registration. Please try again.', 'error')
            current_app.logger.error(f"Registration error: {str(e)}")  # Log the error
            return render_template('register.html', 
                                 username=username, 
                                 email=email)

    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.verify_password(username, password)

        if user:
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.login'))