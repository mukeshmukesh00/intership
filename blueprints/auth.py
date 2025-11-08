# blueprints/auth.py - Authentication blueprint
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.database import get_db
from utils.auth import hash_password, check_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        role = request.form.get('role', '').strip()
        name = request.form.get('name', '').strip()
        
        # Validation errors list
        errors = []
        
        # Validate email
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email.split('@')[1]:
            errors.append('Please enter a valid email address.')
        elif len(email) > 255:
            errors.append('Email is too long (max 255 characters).')
        
        # Validate password
        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        elif len(password) > 128:
            errors.append('Password is too long (max 128 characters).')
        
        # Validate password confirmation
        if not confirm_password:
            errors.append('Please confirm your password.')
        elif password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Validate role
        if not role:
            errors.append('Please select a role.')
        elif role not in ['student', 'company']:
            errors.append('Invalid role selected.')
        
        # Validate name (optional but if provided, should be valid)
        if name and len(name) < 2:
            errors.append('Name should be at least 2 characters long.')
        elif len(name) > 100:
            errors.append('Name is too long (max 100 characters).')
        
        # Check if email already exists
        if email:
            try:
                conn = get_db()
                irs = conn.cursor()
                irs.execute("SELECT id FROM users WHERE email=?", (email,))
                existing_user = irs.fetchone()
                if existing_user:
                    errors.append('Email is already registered. Please use a different email or login.')
            except Exception as e:
                errors.append('Error checking email availability.')
        
        # If there are validation errors, return them
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        # All validation passed, proceed with registration
        hashed_pw = hash_password(password)
        
        try:
            conn = get_db()
            irs = conn.cursor()
            irs.execute("INSERT INTO users (email, password, role, name) VALUES (?, ?, ?, ?)",
                           (email, hashed_pw, role, name))
            conn.commit()
            
            # If student, create empty profile
            if role == 'student':
                user_id = irs.lastrowid
                irs.execute("INSERT INTO profiles (user_id) VALUES (?)", (user_id,))
                conn.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email is already registered. Please use a different email or login.', 'danger')
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        errors = []
        
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email.split('@')[1]:
            errors.append('Please enter a valid email address.')
        
        if not password:
            errors.append('Password is required.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('login.html')
        
        # Attempt login
        try:
            conn = get_db()
            irs = conn.cursor()
            irs.execute("SELECT * FROM users WHERE email=?", (email,))
            user = irs.fetchone()
            
            if user and check_password(password, user['password']):
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['role'] = user['role']
                session['name'] = user['name']
                
                if user['role'] == 'student':
                    # Check if student has CV
                    irs.execute("SELECT * FROM cvs WHERE user_id=?", (user['id'],))
                    cv = irs.fetchone()
                    
                    if not cv:
                        # No CV exists, redirect to CV creation
                        return redirect(url_for('cv.create'))
                    
                    # Redirect to dashboard (skills are now managed through CV)
                    return redirect(url_for('student.dashboard'))
                elif user['role'] == 'company':
                    return redirect(url_for('company.dashboard'))
                elif user['role'] == 'admin':
                    return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.home'))
