# utils/database.py - Database utilities
import sqlite3
from flask import current_app

def init_db():
    """Initialize the database with all required tables and sample data."""
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        irs = conn.cursor()
        
        # Create users table
        irs.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'company', 'admin')),
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create profiles table
        irs.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skills TEXT,
            education TEXT,
            experience TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create internships table
        irs.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            required_skills TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES users (id)
        )
        ''')
        
        # Create applications table
        irs.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            internship_id INTEGER NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (internship_id) REFERENCES internships (id)
        )
        ''')
        
        # Create messages table
        irs.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            internship_id INTEGER NOT NULL,
            content TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id),
            FOREIGN KEY (internship_id) REFERENCES internships (id)
        )
        ''')
        
        # Create CVs table
        irs.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            linkedin_url TEXT,
            github_url TEXT,
            objective TEXT,
            education TEXT,
            education_details TEXT,
            work_experience TEXT,
            projects TEXT,
            certifications TEXT,
            languages TEXT,
            languages_details TEXT,
            interests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Add new columns if they don't exist (for existing databases)
        try:
            irs.execute("ALTER TABLE cvs ADD COLUMN education_details TEXT")
        except:
            pass  # Column already exists
        
        try:
            irs.execute("ALTER TABLE cvs ADD COLUMN languages_details TEXT")
        except:
            pass  # Column already exists
        
        conn.commit()

def get_db():
    """Get database connection with row factory."""
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn
