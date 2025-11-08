# blueprints/company.py - Company blueprint
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from utils.database import get_db

company_bp = Blueprint('company', __name__, url_prefix='/company')

def require_company_auth():
    """Decorator to require company authentication."""
    if 'user_id' not in session or session['role'] != 'company':
        flash('Please log in as a company', 'danger')
        return redirect(url_for('auth.login'))
    return None

@company_bp.route('/dashboard')
def dashboard():
    """Company dashboard."""
    auth_check = require_company_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get company's internships
    irs.execute("SELECT * FROM internships WHERE company_id=?", (session['user_id'],))
    internships_rows = irs.fetchall()
    
    # Convert Row objects to dictionaries
    internships = [dict(row) for row in internships_rows]
    
    # Get applications for each internship
    applications = {}
    for internship in internships:
        irs.execute('''
            SELECT applications.*, users.name as student_name 
            FROM applications 
            JOIN users ON applications.student_id = users.id 
            WHERE internship_id=?
        ''', (internship['id'],))
        app_rows = irs.fetchall()
        # Convert Row objects to dictionaries
        applications[internship['id']] = [dict(row) for row in app_rows]
    
    # Get messages
    irs.execute('''
        SELECT messages.content, messages.sent_at, users.name as receiver_name, internships.title
        FROM messages
        JOIN users ON messages.receiver_id = users.id
        JOIN internships ON messages.internship_id = internships.id
        WHERE messages.sender_id=?
    ''', (session['user_id'],))
    messages_rows = irs.fetchall()
    
    # Convert Row objects to dictionaries
    messages = [dict(row) for row in messages_rows]
    
    return render_template('company_dashboard.html', internships=internships, 
                           applications=applications, messages=messages)

@company_bp.route('/internship/post', methods=['GET', 'POST'])
def post_internship():
    """Post a new internship."""
    auth_check = require_company_auth()
    if auth_check:
        return auth_check
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        required_skills = request.form['required_skills']
        
        if not title:
            flash('Title is required', 'danger')
            return redirect(url_for('company.post_internship'))
        
        try:
            conn = get_db()
            irs = conn.cursor()
            irs.execute("INSERT INTO internships (company_id, title, description, required_skills) VALUES (?, ?, ?, ?)",
                           (session['user_id'], title, description, required_skills))
            conn.commit()
            flash('Internship posted successfully!', 'success')
            return redirect(url_for('company.dashboard'))
        except Exception as e:
            flash(f'Error posting internship: {str(e)}', 'danger')
    
    return render_template('post_internship.html')

@company_bp.route('/application/<int:application_id>/update', methods=['POST'])
def update_application(application_id):
    """Update application status."""
    auth_check = require_company_auth()
    if auth_check:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    status = request.form['status']
    
    # Validate status
    valid_statuses = ['pending', 'accepted', 'rejected']
    if status not in valid_statuses:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    conn = get_db()
    irs = conn.cursor()
    
    # Verify the application belongs to the company
    irs.execute('''
        SELECT internships.company_id 
        FROM applications 
        JOIN internships ON applications.internship_id = internships.id 
        WHERE applications.id=?
    ''', (application_id,))
    app_data = irs.fetchone()
    
    if not app_data or app_data['company_id'] != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        irs.execute("UPDATE applications SET status=? WHERE id=?", (status, application_id))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@company_bp.route('/view-cv/<int:student_id>')
def view_student_cv(student_id):
    """View a student's CV."""
    auth_check = require_company_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get student's CV
    irs.execute("SELECT * FROM cvs WHERE user_id=?", (student_id,))
    cv = irs.fetchone()
    
    if not cv:
        flash('Student has not created a CV yet', 'warning')
        return redirect(url_for('company.dashboard'))
    
    # Get student's basic info
    irs.execute("SELECT name, email FROM users WHERE id=?", (student_id,))
    student = irs.fetchone()
    
    return render_template('cv_view.html', cv=cv, student=student, company_view=True)

@company_bp.route('/internship/<int:internship_id>/delete', methods=['POST'])
def delete_internship(internship_id):
    """Delete an internship and all related data."""
    auth_check = require_company_auth()
    if auth_check:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db()
    irs = conn.cursor()
    
    # Verify the internship belongs to the company
    irs.execute("SELECT company_id, title FROM internships WHERE id=?", (internship_id,))
    internship = irs.fetchone()
    
    if not internship or internship['company_id'] != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Delete related data in the correct order (due to foreign key constraints)
        
        # 1. Delete messages related to this internship
        irs.execute("DELETE FROM messages WHERE internship_id=?", (internship_id,))
        
        # 2. Delete applications for this internship
        irs.execute("DELETE FROM applications WHERE internship_id=?", (internship_id,))
        
        # 3. Delete the internship itself
        irs.execute("DELETE FROM internships WHERE id=?", (internship_id,))
        
        conn.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Internship "{internship["title"]}" deleted successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500