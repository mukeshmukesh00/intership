"""
Test suite for database operations.
Tests database initialization and connection.
"""
import unittest
import sqlite3


class TestDatabaseConnection(unittest.TestCase):
    """Test database connection functionality."""
    
    def test_database_connection_works(self):
        """Test that SQLite database connection works."""
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        
        self.assertIsInstance(conn, sqlite3.Connection,
                            "Should return a SQLite connection")
        
        # Verify connection works
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1,
                       "Connection should be functional")
        
        conn.close()
    
    def test_row_factory_setting(self):
        """Test that row factory can be set to sqlite3.Row."""
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        
        self.assertEqual(conn.row_factory, sqlite3.Row,
                      "Row factory should be set to sqlite3.Row")
        
        conn.close()


class TestDatabaseInitialization(unittest.TestCase):
    """Test database table initialization."""
    
    def setUp(self):
        """Set up test database."""
        self.test_db = ':memory:'
    
    def test_can_create_users_table(self):
        """Test that users table can be created with correct schema."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student', 'company', 'admin')),
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verify table exists
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        ''')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result,
                           "Users table should be created")
        
        # Verify table structure
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        expected_columns = ['id', 'email', 'password', 'role', 'name', 'created_at']
        for col in expected_columns:
            self.assertIn(col, columns,
                        f"Users table should have {col} column")
        
        conn.close()
    
    def test_can_create_profiles_table(self):
        """Test that profiles table can be created."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skills TEXT,
                education TEXT,
                experience TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='profiles'
        ''')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result,
                           "Profiles table should be created")
        
        conn.close()
    
    def test_can_create_internships_table(self):
        """Test that internships table can be created."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
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
        
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='internships'
        ''')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result,
                           "Internships table should be created")
        
        conn.close()
    
    def test_can_create_applications_table(self):
        """Test that applications table can be created."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
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
        
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='applications'
        ''')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result,
                           "Applications table should be created")
        
        conn.close()
    
    def test_can_create_messages_table(self):
        """Test that messages table can be created."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
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
        
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='messages'
        ''')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result,
                           "Messages table should be created")
        
        conn.close()
    
    def test_can_create_cvs_table(self):
        """Test that CVs table can be created."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        cursor.execute('''
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
                work_experience TEXT,
                projects TEXT,
                certifications TEXT,
                languages TEXT,
                interests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='cvs'
        ''')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result,
                           "CVs table should be created")
        
        conn.close()
    
    def test_all_required_tables_can_be_created(self):
        """Test that all required tables can be created."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Create all tables
        tables_sql = [
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skills TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS internships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                required_skills TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                internship_id INTEGER NOT NULL
            )''',
            '''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                internship_id INTEGER NOT NULL
            )''',
            '''CREATE TABLE IF NOT EXISTS cvs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name TEXT NOT NULL
            )'''
        ]
        
        for sql in tables_sql:
            cursor.execute(sql)
        
        conn.commit()
        
        # Verify all tables exist
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table'
        ''')
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'profiles', 'internships', 
                        'applications', 'messages', 'cvs']
        
        for table in expected_tables:
            self.assertIn(table, tables,
                        f"Table {table} should be created")
        
        conn.close()


if __name__ == '__main__':
    unittest.main()
