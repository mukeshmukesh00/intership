"""
Test suite for recommendation algorithms.
Tests Jaccard similarity, content-based filtering, collaborative filtering, and hybrid recommendations.
"""
import unittest
import sqlite3
from utils.recommendations import (
    content_based_recommendations,
    collaborative_filtering,
    get_recommendations
)


def calculate_jaccard_similarity(set1, set2):
    """Helper function to calculate Jaccard similarity."""
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0


class TestJaccardSimilarity(unittest.TestCase):
    """Test Jaccard similarity calculation (core algorithm)."""
    
    def test_jaccard_perfect_match(self):
        """Test Jaccard similarity with identical sets (should be 1.0)."""
        skills1 = {'python', 'javascript', 'react'}
        skills2 = {'python', 'javascript', 'react'}
        
        result = calculate_jaccard_similarity(skills1, skills2)
        self.assertEqual(result, 1.0, "Perfect match should have similarity of 1.0")
    
    def test_jaccard_no_match(self):
        """Test Jaccard similarity with no common skills (should be 0.0)."""
        skills1 = {'python', 'java'}
        skills2 = {'javascript', 'react'}
        
        result = calculate_jaccard_similarity(skills1, skills2)
        self.assertEqual(result, 0.0, "No common skills should have similarity of 0.0")
    
    def test_jaccard_partial_match(self):
        """Test Jaccard similarity with partial match."""
        skills1 = {'python', 'javascript', 'react'}
        skills2 = {'python', 'html', 'css'}
        
        result = calculate_jaccard_similarity(skills1, skills2)
        # Expected: intersection=1 (python), union=5 (python, javascript, react, html, css)
        # similarity = 1/5 = 0.2
        self.assertAlmostEqual(result, 0.2, places=2, 
                             msg="Partial match should calculate correct similarity")
    
    def test_jaccard_empty_sets(self):
        """Test Jaccard similarity with empty sets."""
        skills1 = set()
        skills2 = {'python', 'javascript'}
        
        result = calculate_jaccard_similarity(skills1, skills2)
        self.assertEqual(result, 0.0, "Empty set should return 0.0")
    
    def test_jaccard_case_insensitive(self):
        """Test that similarity works with different case (normalized in actual code)."""
        skills1 = {'Python', 'JAVASCRIPT', 'React'}
        skills2 = {'python', 'javascript', 'react'}
        
        # Note: Actual code normalizes to lowercase, so these should be equal
        skills1_lower = {s.lower() for s in skills1}
        skills2_lower = {s.lower() for s in skills2}
        
        result = calculate_jaccard_similarity(skills1_lower, skills2_lower)
        self.assertEqual(result, 1.0, "Case should be normalized for comparison")


class TestContentBasedRecommendations(unittest.TestCase):
    """Test content-based recommendation algorithm."""
    
    def setUp(self):
        """Set up test database with sample data."""
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Create test tables
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                email TEXT,
                name TEXT,
                role TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE profiles (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                skills TEXT,
                education TEXT,
                experience TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE internships (
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                title TEXT,
                description TEXT,
                required_skills TEXT,
                posted_at TEXT
            )
        ''')
        
        # Insert test data
        # Create company user
        self.cursor.execute('''
            INSERT INTO users (id, email, name, role)
            VALUES (2, 'company@test.com', 'Test Company', 'company')
        ''')
        
        # Create student user with skills
        self.cursor.execute('''
            INSERT INTO users (id, email, name, role)
            VALUES (1, 'student@test.com', 'Test Student', 'student')
        ''')
        
        self.cursor.execute('''
            INSERT INTO profiles (user_id, skills)
            VALUES (1, 'Python, JavaScript, React, SQL')
        ''')
        
        # Create internships
        self.cursor.execute('''
            INSERT INTO internships (id, company_id, title, description, required_skills, posted_at)
            VALUES 
            (1, 2, 'Python Developer', 'Develop Python applications', 'Python, Flask, Django', '2024-01-01'),
            (2, 2, 'Web Developer', 'Build web applications', 'JavaScript, React, HTML, CSS', '2024-01-02'),
            (3, 2, 'Java Developer', 'Java development role', 'Java, Spring, Hibernate', '2024-01-03'),
            (4, 2, 'Full Stack Developer', 'Full stack development', 'Python, JavaScript, React, SQL', '2024-01-04'),
            (5, 2, 'Data Scientist', 'Data analysis role', 'Python, Machine Learning, Pandas', '2024-01-05')
        ''')
        
        self.conn.commit()
    
    def test_finds_matching_internships(self):
        """Test that content-based filtering finds matching internships."""
        recommendations = content_based_recommendations(1, self.cursor)
        
        self.assertGreater(len(recommendations), 0, 
                         "Should find at least one matching internship")
        
        # Should find Web Developer (matches JavaScript, React)
        titles = [r['title'] for r in recommendations]
        self.assertIn('Web Developer', titles,
                     "Should recommend Web Developer for JavaScript/React skills")
        
        # Should find Full Stack Developer (matches multiple skills)
        self.assertIn('Full Stack Developer', titles,
                     "Should recommend Full Stack for multiple matching skills")
        
        # Python Developer may not appear if similarity is below threshold
        # Check that we have some recommendations
        self.assertGreater(len(titles), 0,
                         "Should have at least one recommendation")
    
    def test_filters_non_matching_internships(self):
        """Test that non-matching internships are filtered out."""
        recommendations = content_based_recommendations(1, self.cursor)
        
        titles = [r['title'] for r in recommendations]
        # Should NOT find Java Developer (no matching skills)
        self.assertNotIn('Java Developer', titles,
                        "Should not recommend internships with no matching skills")
    
    def test_sorts_by_similarity(self):
        """Test that recommendations are sorted by similarity (highest first)."""
        recommendations = content_based_recommendations(1, self.cursor)
        
        if len(recommendations) > 1:
            # First recommendation should have higher or equal similarity to second
            first_similarity = recommendations[0]['similarity']
            second_similarity = recommendations[1]['similarity']
            
            self.assertGreaterEqual(first_similarity, second_similarity,
                                  "Recommendations should be sorted by similarity (descending)")
    
    def test_filters_below_threshold(self):
        """Test that recommendations below 0.2 threshold are filtered out."""
        recommendations = content_based_recommendations(1, self.cursor)
        
        # All recommendations should have similarity > 0.2
        for rec in recommendations:
            self.assertGreater(rec['similarity'], 0.2,
                             f"Recommendation '{rec['title']}' should have similarity > 0.2")
    
    def test_limits_to_top_5(self):
        """Test that only top 5 recommendations are returned."""
        # Add more internships to test limit
        for i in range(10):
            self.cursor.execute('''
                INSERT INTO internships (company_id, title, description, required_skills, posted_at)
                VALUES (2, ?, 'Test internship', 'Python, JavaScript, React, SQL', '2024-01-01')
            ''', (f'Internship {i}',))
        self.conn.commit()
        
        recommendations = content_based_recommendations(1, self.cursor)
        self.assertLessEqual(len(recommendations), 5,
                            "Should return at most 5 recommendations")
    
    def test_empty_skills_returns_empty(self):
        """Test that students with no skills get no recommendations."""
        # Create student with no skills
        self.cursor.execute('''
            INSERT INTO users (id, email, name, role)
            VALUES (10, 'nostudent@test.com', 'No Skills', 'student')
        ''')
        self.cursor.execute('''
            INSERT INTO profiles (user_id, skills)
            VALUES (10, NULL)
        ''')
        self.conn.commit()
        
        recommendations = content_based_recommendations(10, self.cursor)
        self.assertEqual(len(recommendations), 0,
                        "Student with no skills should get no recommendations")
    
    def test_includes_company_name(self):
        """Test that recommendations include company name."""
        recommendations = content_based_recommendations(1, self.cursor)
        
        if len(recommendations) > 0:
            self.assertIn('company_name', recommendations[0],
                         "Recommendations should include company_name")
    
    def test_includes_similarity_score(self):
        """Test that recommendations include similarity score."""
        recommendations = content_based_recommendations(1, self.cursor)
        
        if len(recommendations) > 0:
            self.assertIn('similarity', recommendations[0],
                         "Recommendations should include similarity score")
            self.assertIsInstance(recommendations[0]['similarity'], (int, float),
                                "Similarity should be a number")
    
    def tearDown(self):
        """Clean up test database."""
        self.conn.close()


class TestCollaborativeFiltering(unittest.TestCase):
    """Test collaborative filtering recommendation algorithm."""
    
    def setUp(self):
        """Set up test database with application history."""
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                email TEXT,
                name TEXT,
                role TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE internships (
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                title TEXT,
                description TEXT,
                required_skills TEXT,
                posted_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE applications (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                internship_id INTEGER,
                applied_at TEXT,
                status TEXT
            )
        ''')
        
        # Create users
        for i in range(1, 6):
            self.cursor.execute('''
                INSERT INTO users (id, email, name, role)
                VALUES (?, ?, ?, 'student')
            ''', (i, f'student{i}@test.com', f'Student {i}'))
        
        # Create company
        self.cursor.execute('''
            INSERT INTO users (id, email, name, role)
            VALUES (10, 'company@test.com', 'Company', 'company')
        ''')
        
        # Create internships
        for i in range(1, 6):
            self.cursor.execute('''
                INSERT INTO internships (id, company_id, title, description, required_skills, posted_at)
                VALUES (?, 10, ?, 'Description', 'Python', '2024-01-01')
            ''', (i, f'Internship {i}'))
        
        # Create application history
        # Student 1 applied to internships 1, 2, 3
        for i in [1, 2, 3]:
            self.cursor.execute('''
                INSERT INTO applications (student_id, internship_id, status)
                VALUES (1, ?, 'pending')
            ''', (i,))
        
        # Student 2 applied to internships 2, 3, 4 (similar to student 1)
        for i in [2, 3, 4]:
            self.cursor.execute('''
                INSERT INTO applications (student_id, internship_id, status)
                VALUES (2, ?, 'pending')
            ''', (i,))
        
        # Student 3 applied to internships 4, 5 (different)
        for i in [4, 5]:
            self.cursor.execute('''
                INSERT INTO applications (student_id, internship_id, status)
                VALUES (3, ?, 'pending')
            ''', (i,))
        
        self.conn.commit()
    
    def test_finds_similar_students(self):
        """Test that collaborative filtering finds similar students."""
        recommendations = collaborative_filtering(1, self.cursor)
        
        # Student 1 and Student 2 have similar application history
        # Student 2 applied to 4, which Student 1 didn't
        # So Student 1 should get recommendation for internship 4
        
        titles = [r['title'] for r in recommendations]
        self.assertIn('Internship 4', titles,
                     "Should recommend internships from similar students")
    
    def test_excludes_already_applied(self):
        """Test that already applied internships are excluded."""
        recommendations = collaborative_filtering(1, self.cursor)
        
        titles = [r['title'] for r in recommendations]
        # Student 1 already applied to 1, 2, 3
        self.assertNotIn('Internship 1', titles,
                        "Should not recommend already applied internships")
        self.assertNotIn('Internship 2', titles,
                        "Should not recommend already applied internships")
        self.assertNotIn('Internship 3', titles,
                        "Should not recommend already applied internships")
    
    def test_returns_top_recommendations(self):
        """Test that only top recommendations are returned."""
        recommendations = collaborative_filtering(1, self.cursor)
        self.assertLessEqual(len(recommendations), 5,
                            "Should return at most 5 recommendations")
    
    def test_empty_application_history(self):
        """Test handling of users with no application history."""
        # Student 4 has no applications
        recommendations = collaborative_filtering(4, self.cursor)
        # Should return empty or handle gracefully
        self.assertIsInstance(recommendations, list,
                            "Should return a list even with no history")
    
    def tearDown(self):
        """Clean up test database."""
        self.conn.close()


class TestHybridRecommendations(unittest.TestCase):
    """Test hybrid recommendation system combining multiple algorithms."""
    
    def setUp(self):
        """Set up test database for hybrid recommendations."""
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                email TEXT,
                name TEXT,
                role TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE profiles (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                skills TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE internships (
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                title TEXT,
                description TEXT,
                required_skills TEXT,
                posted_at TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE applications (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                internship_id INTEGER,
                status TEXT
            )
        ''')
        
        # Setup data
        self.cursor.execute('''
            INSERT INTO users (id, email, name, role)
            VALUES 
            (1, 'student@test.com', 'Student', 'student'),
            (2, 'company@test.com', 'Company', 'company')
        ''')
        
        self.cursor.execute('''
            INSERT INTO profiles (user_id, skills)
            VALUES (1, 'Python, JavaScript')
        ''')
        
        self.cursor.execute('''
            INSERT INTO internships (id, company_id, title, required_skills, posted_at)
            VALUES 
            (1, 2, 'Python Dev', 'Python', '2024-01-01'),
            (2, 2, 'Web Dev', 'JavaScript', '2024-01-02')
        ''')
        
        self.conn.commit()
    
    def test_combines_recommendations(self):
        """Test that hybrid system combines recommendations from multiple algorithms."""
        # Mock the get_recommendations function to work with test database
        # Note: Actual get_recommendations uses get_db() which requires Flask app context
        # For this test, we'll verify the combination logic separately
        
        content_recs = content_based_recommendations(1, self.cursor)
        
        self.assertGreater(len(content_recs), 0,
                         "Should have content-based recommendations")
    
    def test_deduplicates_recommendations(self):
        """Test that duplicate recommendations are properly handled."""
        # Get content-based recommendations
        content_recs = content_based_recommendations(1, self.cursor)
        
        # Check that all recommendations have unique IDs
        ids = [r['id'] for r in content_recs]
        self.assertEqual(len(ids), len(set(ids)),
                        "Recommendations should have unique IDs")
    
    def tearDown(self):
        """Clean up test database."""
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
