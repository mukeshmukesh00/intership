#!/usr/bin/env python3
"""
Test script to verify the sqlite3.Row conversion fix
"""
import sqlite3
from datetime import datetime

def test_sqlite_row_conversion():
    """Test the sqlite3.Row to dict conversion logic"""
    
    # Create a test database in memory with row_factory to return Row objects
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row  # This makes fetchone() return Row objects
    irs = conn.cursor()
    
    # Create a test table
    irs.execute('''
        CREATE TABLE test_cvs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            full_name TEXT,
            updated_at TIMESTAMP
        )
    ''')
    
    # Insert test data
    irs.execute('''
        INSERT INTO test_cvs (user_id, full_name, updated_at)
        VALUES (1, 'Test User', '2024-01-15 14:30:25')
    ''')
    
    # Fetch data (this returns a sqlite3.Row object)
    irs.execute("SELECT * FROM test_cvs WHERE user_id=?", (1,))
    cv_row = irs.fetchone()
    
    print("Original sqlite3.Row:")
    print(f"Type: {type(cv_row)}")
    print(f"updated_at: {cv_row['updated_at']} (type: {type(cv_row['updated_at'])})")
    
    # Test the conversion logic from student.py
    cv = None
    if cv_row:
        cv = dict(cv_row)
        print(f"\nAfter dict conversion:")
        print(f"Type: {type(cv)}")
        print(f"updated_at: {cv['updated_at']} (type: {type(cv['updated_at'])})")
        
        # Convert string timestamps to datetime objects
        if cv['updated_at']:
            try:
                if isinstance(cv['updated_at'], str):
                    cv['updated_at'] = datetime.strptime(cv['updated_at'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                cv['updated_at'] = None
        
        print(f"\nAfter datetime conversion:")
        print(f"updated_at: {cv['updated_at']} (type: {type(cv['updated_at'])})")
        
        # Test strftime
        if cv['updated_at']:
            formatted = cv['updated_at'].strftime('%B %d, %Y')
            print(f"Formatted: {formatted}")
            print("✅ Conversion successful!")
        else:
            print("❌ Conversion failed!")
    
    conn.close()

if __name__ == "__main__":
    test_sqlite_row_conversion()
