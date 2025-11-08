# utils/auth.py - Authentication utilities
from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db

def create_sample_data():
    """Create sample data for demonstration."""
    conn = get_db()
    irs = conn.cursor()
    
    # Create admin user if not exists
    irs.execute("SELECT * FROM users WHERE email=?", ('admin@internhub.com',))
    admin = irs.fetchone()
    if not admin:
        hashed_pw = generate_password_hash('admin123')
        irs.execute("INSERT INTO users (email, password, role, name) VALUES (?, ?, ?, ?)", 
                       ('admin@internhub.com', hashed_pw, 'admin', 'Admin User'))
    
    # Create sample data for demonstration
    irs.execute("SELECT * FROM users WHERE role='student'")
    if not irs.fetchone():
        hashed_pw = generate_password_hash('student123')
        irs.execute("INSERT INTO users (email, password, role, name) VALUES (?, ?, ?, ?)", 
                       ('student@example.com', hashed_pw, 'student', 'John Doe'))
        student_id = irs.lastrowid
        irs.execute("INSERT INTO profiles (user_id, skills, education, experience) VALUES (?, ?, ?, ?)",
                       (student_id, 'Python, Flask, SQL', 'Computer Science BSc', 'Part-time web developer'))
        
    irs.execute("SELECT * FROM users WHERE role='company'")
    if not irs.fetchone():
        hashed_pw = generate_password_hash('company123')
        irs.execute("INSERT INTO users (email, password, role, name) VALUES (?, ?, ?, ?)", 
                       ('company@example.com', hashed_pw, 'company', 'TechCorp Inc'))
        company_id = irs.lastrowid
        irs.execute("INSERT INTO internships (company_id, title, description, required_skills) VALUES (?, ?, ?, ?)",
                       (company_id, 'Web Development Intern', 'Develop web applications using Flask', 'Python, Flask, HTML, CSS'))
        irs.execute("INSERT INTO internships (company_id, title, description, required_skills) VALUES (?, ?, ?, ?)",
                       (company_id, 'Data Science Intern', 'Analyze datasets and build ML models', 'Python, Pandas, Machine Learning'))
    
    conn.commit()

def hash_password(password):
    """Hash a password for storage."""
    return generate_password_hash(password)

def check_password(user_password, hashed_password):
    """Check if provided password matches the hash."""
    return check_password_hash(hashed_password, user_password)
