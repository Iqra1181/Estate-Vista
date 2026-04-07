# routes/auth.py
# Handles: User Signup, Login, Logout
# Uses Flask sessions to track logged-in users
# Uses Werkzeug to hash/check passwords securely

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from realestate.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint — a mini Flask app that groups related routes
auth_bp = Blueprint('auth', __name__)


# ─────────────────────────────────────────────
# SIGNUP ROUTE
# GET  → show the signup form
# POST → process form, create user in DB
# ─────────────────────────────────────────────
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('properties.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # ── Validation ──────────────────────────────────
        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/signup.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('auth/signup.html')

        # Check if email already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('An account with this email already exists.', 'danger')
            return render_template('auth/signup.html')

        # ── Create User ──────────────────────────────────
        # Hash the password before storing (NEVER store plain text passwords!)
        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


# ─────────────────────────────────────────────
# LOGIN ROUTE
# ─────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('properties.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Find user by email
        user = User.query.filter_by(email=email).first()

        # Check if user exists AND password matches
        if user and check_password_hash(user.password, password):
            # Save user info in session (like a cookie stored server-side)
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}! 🏠', 'success')
            return redirect(url_for('properties.index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


# ─────────────────────────────────────────────
# LOGOUT ROUTE
# ─────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()  # Remove all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('properties.index'))
