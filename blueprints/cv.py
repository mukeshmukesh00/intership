# blueprints/cv.py - CV management blueprint
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from utils.database import get_db
from datetime import datetime

cv_bp = Blueprint('cv', __name__, url_prefix='/cv')

def require_student_auth():
    """Decorator to require student authentication."""
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please log in as a student', 'danger')
        return redirect(url_for('auth.login'))
    return None

@cv_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new CV."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Check if CV already exists
    irs.execute("SELECT * FROM cvs WHERE user_id=?", (session['user_id'],))
    existing_cv = irs.fetchone()
    
    if existing_cv:
        flash('You already have a CV. You can edit it instead.', 'info')
        return redirect(url_for('cv.edit'))
    
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form.get('phone', '')
            address = request.form.get('address', '')
            linkedin_url = request.form.get('linkedin_url', '')
            github_url = request.form.get('github_url', '')
            objective = request.form.get('objective', '')
            education = request.form.get('education', '')
            education_details = request.form.get('education_details', '')
            work_experience = request.form.get('work_experience', '')
            projects = request.form.get('projects', '')
            certifications = request.form.get('certifications', '')  # This now contains skills
            languages = request.form.get('languages', '')
            languages_details = request.form.get('languages_details', '')
            interests = request.form.get('interests', '')
            
            if not full_name or not email:
                flash('Full name and email are required', 'danger')
                return redirect(url_for('cv.create'))
            
            # Insert CV into database
            irs.execute('''
                INSERT INTO cvs (user_id, full_name, email, phone, address, linkedin_url, 
                               github_url, objective, education, education_details, work_experience, projects, 
                               certifications, languages, languages_details, interests)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], full_name, email, phone, address, linkedin_url,
                  github_url, objective, education, education_details, work_experience, projects,
                  certifications, languages, languages_details, interests))
            
            # Sync skills to profile (certifications field contains skills)
            irs.execute("SELECT * FROM profiles WHERE user_id=?", (session['user_id'],))
            profile = irs.fetchone()
            if profile:
                irs.execute("UPDATE profiles SET skills=?, education=?, experience=? WHERE user_id=?", 
                              (certifications, education, work_experience, session['user_id']))
            
            conn.commit()
            flash('CV created successfully!', 'success')
            return redirect(url_for('cv.view'))
            
        except Exception as e:
            flash(f'Error creating CV: {str(e)}', 'danger')
    
    return render_template('cv_create.html')

@cv_bp.route('/edit', methods=['GET', 'POST'])
def edit():
    """Edit existing CV."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get existing CV
    irs.execute("SELECT * FROM cvs WHERE user_id=?", (session['user_id'],))
    cv = irs.fetchone()
    
    if not cv:
        flash('No CV found. Please create one first.', 'info')
        return redirect(url_for('cv.create'))
    
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form.get('phone', '')
            address = request.form.get('address', '')
            linkedin_url = request.form.get('linkedin_url', '')
            github_url = request.form.get('github_url', '')
            objective = request.form.get('objective', '')
            education = request.form.get('education', '')
            education_details = request.form.get('education_details', '')
            work_experience = request.form.get('work_experience', '')
            projects = request.form.get('projects', '')
            certifications = request.form.get('certifications', '')  # This now contains skills
            languages = request.form.get('languages', '')
            languages_details = request.form.get('languages_details', '')
            interests = request.form.get('interests', '')
            
            if not full_name or not email:
                flash('Full name and email are required', 'danger')
                return redirect(url_for('cv.edit'))
            
            # Update CV in database
            irs.execute('''
                UPDATE cvs SET full_name=?, email=?, phone=?, address=?, linkedin_url=?, 
                             github_url=?, objective=?, education=?, education_details=?, work_experience=?, 
                             projects=?, certifications=?, languages=?, languages_details=?, interests=?, 
                             updated_at=CURRENT_TIMESTAMP
                WHERE user_id=?
            ''', (full_name, email, phone, address, linkedin_url, github_url,
                  objective, education, education_details, work_experience, projects, certifications,
                  languages, languages_details, interests, session['user_id']))
            
            # Sync skills to profile (certifications field contains skills)
            irs.execute("SELECT * FROM profiles WHERE user_id=?", (session['user_id'],))
            profile = irs.fetchone()
            if profile:
                irs.execute("UPDATE profiles SET skills=?, education=?, experience=? WHERE user_id=?", 
                              (certifications, education, work_experience, session['user_id']))
            
            conn.commit()
            flash('CV updated successfully!', 'success')
            return redirect(url_for('cv.view'))
            
        except Exception as e:
            flash(f'Error updating CV: {str(e)}', 'danger')
    
    return render_template('cv_edit.html', cv=cv)

@cv_bp.route('/view')
def view():
    """View CV."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get CV
    irs.execute("SELECT * FROM cvs WHERE user_id=?", (session['user_id'],))
    cv = irs.fetchone()
    
    if not cv:
        flash('No CV found. Please create one first.', 'info')
        return redirect(url_for('cv.create'))
    
    return render_template('cv_view.html', cv=cv)

@cv_bp.route('/download')
def download():
    """Download CV as PDF (placeholder for future implementation)."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    flash('PDF download feature coming soon!', 'info')
    return redirect(url_for('cv.view'))

@cv_bp.route('/delete', methods=['POST'])
def delete():
    """Delete CV."""
    auth_check = require_student_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    try:
        irs.execute("DELETE FROM cvs WHERE user_id=?", (session['user_id'],))
        conn.commit()
        flash('CV deleted successfully!', 'success')
        return redirect(url_for('cv.create'))
    except Exception as e:
        flash(f'Error deleting CV: {str(e)}', 'danger')
        return redirect(url_for('cv.view'))
