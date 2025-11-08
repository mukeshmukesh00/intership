"""
Test suite for authentication functions.
Tests password hashing and verification.
"""
import unittest
from utils.auth import hash_password, check_password


class TestPasswordHashing(unittest.TestCase):
    """Test password hashing functionality."""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string."""
        hashed = hash_password('testpassword123')
        self.assertIsInstance(hashed, str,
                            "Hash should be a string")
        self.assertGreater(len(hashed), 0,
                         "Hash should not be empty")
    
    def test_hash_password_different_inputs_produce_different_hashes(self):
        """Test that different passwords produce different hashes."""
        hash1 = hash_password('password1')
        hash2 = hash_password('password2')
        
        self.assertNotEqual(hash1, hash2,
                          "Different passwords should produce different hashes")
    
    def test_hash_password_same_input_produces_different_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        # Same password should produce different hashes due to salting
        hash1 = hash_password('samepassword')
        hash2 = hash_password('samepassword')
        
        # They should be different due to salt
        self.assertNotEqual(hash1, hash2,
                          "Same password should produce different hashes (salted)")
    
    def test_hash_password_handles_special_characters(self):
        """Test that password hashing handles special characters."""
        special_password = 'p@ssw0rd!$%^&*()'
        hashed = hash_password(special_password)
        
        self.assertIsInstance(hashed, str,
                            "Should handle special characters in password")
        self.assertTrue(check_password(special_password, hashed),
                       "Should verify password with special characters")


class TestPasswordVerification(unittest.TestCase):
    """Test password verification functionality."""
    
    def test_check_password_correct_password_returns_true(self):
        """Test that correct password returns True."""
        password = 'correctpassword'
        hashed = hash_password(password)
        
        result = check_password(password, hashed)
        self.assertTrue(result,
                      "Correct password should return True")
    
    def test_check_password_incorrect_password_returns_false(self):
        """Test that incorrect password returns False."""
        password = 'correctpassword'
        wrong_password = 'wrongpassword'
        hashed = hash_password(password)
        
        result = check_password(wrong_password, hashed)
        self.assertFalse(result,
                        "Incorrect password should return False")
    
    def test_check_password_empty_password(self):
        """Test handling of empty password."""
        hashed = hash_password('somepassword')
        
        result = check_password('', hashed)
        self.assertFalse(result,
                        "Empty password should return False")
    
    def test_check_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = 'Password123'
        wrong_case = 'password123'
        hashed = hash_password(password)
        
        result = check_password(wrong_case, hashed)
        self.assertFalse(result,
                        "Password verification should be case-sensitive")
    
    def test_hash_and_verify_round_trip(self):
        """Test complete flow: hash password then verify it."""
        original_password = 'mysecretpassword123'
        
        # Hash the password
        hashed = hash_password(original_password)
        
        # Verify with original password
        is_valid = check_password(original_password, hashed)
        
        self.assertTrue(is_valid,
                      "Should be able to verify password after hashing")
        
        # Verify with wrong password
        is_invalid = check_password('wrongpassword', hashed)
        
        self.assertFalse(is_invalid,
                        "Should reject wrong password")


if __name__ == '__main__':
    unittest.main()
