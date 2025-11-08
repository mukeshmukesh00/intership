# blueprints/messaging.py - Messaging blueprint
from flask import Blueprint, request, session, jsonify

messaging_bp = Blueprint('messaging', __name__, url_prefix='/message')

@messaging_bp.route('/send', methods=['POST'])
def send_message():
    """Send a message."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    receiver_id = request.form['receiver_id']
    internship_id = request.form['internship_id']
    content = request.form['content']
    
    if not content:
        return jsonify({'success': False, 'message': 'Message content is required'}), 400
    
    from utils.database import get_db
    conn = get_db()
    irs = conn.cursor()
    
    try:
        irs.execute("INSERT INTO messages (sender_id, receiver_id, internship_id, content) VALUES (?, ?, ?, ?)",
                       (session['user_id'], receiver_id, internship_id, content))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
