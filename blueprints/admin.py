# blueprints/admin.py - Admin blueprint
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from utils.database import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin_auth():
    """Decorator to require admin authentication."""
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Please log in as an admin', 'danger')
        return redirect(url_for('auth.login'))
    return None

@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard."""
    auth_check = require_admin_auth()
    if auth_check:
        return auth_check
    
    conn = get_db()
    irs = conn.cursor()
    
    # Get all users
    irs.execute("SELECT * FROM users")
    users = irs.fetchall()
    
    # Get all internships
    irs.execute("SELECT * FROM internships")
    internships = irs.fetchall()
    
    # Get system stats
    irs.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = irs.fetchone()['total_users']
    
    irs.execute("SELECT COUNT(*) as total_internships FROM internships")
    total_internships = irs.fetchone()['total_internships']
    
    irs.execute("SELECT COUNT(*) as total_applications FROM applications")
    total_applications = irs.fetchone()['total_applications']
    
    return render_template('admin_dashboard.html', users=users, internships=internships, 
                           total_users=total_users, total_internships=total_internships, 
                           total_applications=total_applications)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user."""
    auth_check = require_admin_auth()
    if auth_check:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db()
    irs = conn.cursor()
    
    try:
        # Delete user and related data
        irs.execute("DELETE FROM users WHERE id=?", (user_id,))
        
        # Also delete related profile, applications, messages
        irs.execute("DELETE FROM profiles WHERE user_id=?", (user_id,))
        irs.execute("DELETE FROM applications WHERE student_id=?", (user_id,))
        irs.execute("DELETE FROM messages WHERE sender_id=? OR receiver_id=?", (user_id, user_id))
        
        # If company, delete their internships
        irs.execute("DELETE FROM internships WHERE company_id=?", (user_id,))
        
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/internship/<int:internship_id>/delete', methods=['POST'])
def delete_internship(internship_id):
    """Delete an internship."""
    auth_check = require_admin_auth()
    if auth_check:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    conn = get_db()
    irs = conn.cursor()
    
    try:
        # Delete internship and related applications/messages
        irs.execute("DELETE FROM internships WHERE id=?", (internship_id,))
        irs.execute("DELETE FROM applications WHERE internship_id=?", (internship_id,))
        irs.execute("DELETE FROM messages WHERE internship_id=?", (internship_id,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
