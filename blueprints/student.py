# blueprints/student.py - Student blueprint
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.database import get_db
from utils.recommendations import get_recommendations
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/student')

def require_student_auth():
    """Decorator to require student authentication."""
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please log in as a student', 'danger')
        return redirect(url_for('auth.login'))
    return None

@student_bp.route('/dashboard')
def dashboard():
    """Student dashboard."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get student profile
    irs.execute("SELECT * FROM profiles WHERE user_id=?", (session['user_id'],))
    profile = irs.fetchone()
    
    # Get student CV
    irs.execute("SELECT * FROM cvs WHERE user_id=?", (session['user_id'],))
    cv_row = irs.fetchone()
    
    # Convert sqlite3.Row to dict and handle datetime conversion
    cv = None
    if cv_row:
        cv = dict(cv_row)
        # Convert string timestamps to datetime objects if CV exists
        if cv['updated_at']:
            try:
                # Handle both string and datetime formats
                if isinstance(cv['updated_at'], str):
                    cv['updated_at'] = datetime.strptime(cv['updated_at'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                # If parsing fails, set to None
                cv['updated_at'] = None
    
    # Note: Skills are now managed through CV creation
    
    # Get applications
    irs.execute('''
        SELECT internships.title, applications.status, applications.applied_at 
        FROM applications 
        JOIN internships ON applications.internship_id = internships.id 
        WHERE student_id=?
    ''', (session['user_id'],))
    applications = irs.fetchall()
    
    # Get recommended internships
    recommendations = get_recommendations(session['user_id'])
    
    # Get messages
    irs.execute('''
        SELECT messages.content, messages.sent_at, users.name as sender_name, internships.title
        FROM messages
        JOIN users ON messages.sender_id = users.id
        JOIN internships ON messages.internship_id = internships.id
        WHERE messages.receiver_id=?
    ''', (session['user_id'],))
    messages = irs.fetchall()
    
    return render_template('student_dashboard.html', profile=profile, cv=cv, applications=applications, 
                           recommendations=recommendations, messages=messages)


@student_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Student profile management."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get student CV
    irs.execute("SELECT * FROM cvs WHERE user_id=?", (session['user_id'],))
    cv = irs.fetchone()
    
    if request.method == 'POST':
        # Only allow manual profile updates if no CV exists
        if not cv:
            skills = request.form['skills']
            education = request.form['education']
            experience = request.form['experience']
            
            try:
                irs.execute("UPDATE profiles SET skills=?, education=?, experience=? WHERE user_id=?", 
                               (skills, education, experience, session['user_id']))
                conn.commit()
                flash('Profile updated successfully!', 'success')
            except Exception as e:
                flash(f'Error updating profile: {str(e)}', 'danger')
        else:
            flash('Profile is synced with your CV. Please update your CV instead.', 'info')
        
        return redirect(url_for('student.profile'))
    
    irs.execute("SELECT * FROM profiles WHERE user_id=?", (session['user_id'],))
    profile = irs.fetchone()
    return render_template('student_profile.html', profile=profile, cv=cv)

@student_bp.route('/apply/<int:internship_id>', methods=['POST'])
def apply_internship(internship_id):
    """Apply to an internship."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Check if already applied
    irs.execute("SELECT * FROM applications WHERE student_id=? AND internship_id=?", 
                   (session['user_id'], internship_id))
    if irs.fetchone():
        flash('You have already applied to this internship', 'warning')
        return redirect(url_for('main.internships'))
    
    try:
        irs.execute("INSERT INTO applications (student_id, internship_id) VALUES (?, ?)", 
                       (session['user_id'], internship_id))
        conn.commit()
        flash('Application submitted successfully!', 'success')
    except Exception as e:
        flash(f'Error applying: {str(e)}', 'danger')
    
    return redirect(url_for('main.internships'))
