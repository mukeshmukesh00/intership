# app_new.py - Refactored Flask application using blueprints
from flask import Flask
from utils.database import init_db
from utils.auth import create_sample_data

# Import blueprints
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.student import student_bp
from blueprints.company import company_bp
from blueprints.admin import admin_bp
from blueprints.messaging import messaging_bp
from blueprints.cv import cv_bp

def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config['DATABASE'] = 'internship.db'
    
    # Initialize database
    with app.app_context():
        init_db()
        create_sample_data()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(cv_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
