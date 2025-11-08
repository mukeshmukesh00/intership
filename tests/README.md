# Test Suite Documentation

This directory contains the formal test suite for the Internship Recommendation System project.

## 📋 Overview

The test suite demonstrates the **testing phase** of software development lifecycle (SDLC) as required by the project policy.

## 🧪 Test Files

### 1. `test_recommendations.py`
**Tests the core recommendation algorithms:**
- ✅ Jaccard Similarity calculation
- ✅ Content-based filtering algorithm
- ✅ Collaborative filtering algorithm
- ✅ Hybrid recommendation system
- ✅ Edge cases and error handling

**Key Test Cases:**
- Perfect match similarity (should be 1.0)
- No match similarity (should be 0.0)
- Partial match calculations
- Threshold filtering (0.2 for content-based)
- Top 5 limit enforcement
- Empty input handling

### 2. `test_auth.py`
**Tests authentication functions:**
- ✅ Password hashing
- ✅ Password verification
- ✅ Security features (salting, case sensitivity)
- ✅ Edge cases (empty passwords, special characters)

### 3. `test_database.py`
**Tests database operations:**
- ✅ Database connection
- ✅ Table creation
- ✅ Schema validation
- ✅ All required tables exist

## 🚀 Running Tests

### Run All Tests
```bash
python -m unittest discover tests
```

### Run Specific Test File
```bash
python -m unittest tests.test_recommendations
python -m unittest tests.test_auth
python -m unittest tests.test_database
```

### Run with Verbose Output
```bash
python -m unittest discover tests -v
```

### Run Specific Test Case
```bash
python -m unittest tests.test_recommendations.TestJaccardSimilarity
```

## ✅ Expected Output

When all tests pass:
```
test_check_password_case_sensitive ... ok
test_check_password_correct_password_returns_true ... ok
test_check_password_incorrect_password_returns_false ... ok
test_hash_and_verify_round_trip ... ok
test_hash_password_different_inputs_produce_different_hashes ... ok
test_hash_password_returns_string ... ok
test_jaccard_empty_sets ... ok
test_jaccard_no_match ... ok
test_jaccard_partial_match ... ok
test_jaccard_perfect_match ... ok
...

----------------------------------------------------------------------
Ran XX tests in X.XXXs

OK
```

## 📊 Test Coverage

### Algorithm Tests (Priority 1 - Core Feature)
- ✅ Jaccard Similarity: 5 test cases
- ✅ Content-Based Recommendations: 8 test cases
- ✅ Collaborative Filtering: 4 test cases
- ✅ Hybrid System: 2 test cases

### Authentication Tests
- ✅ Password Hashing: 4 test cases
- ✅ Password Verification: 5 test cases

### Database Tests
- ✅ Connection: 2 test cases
- ✅ Initialization: 7 test cases

**Total Test Cases: 37+**

## 🎯 Test Philosophy

1. **Test Core Algorithms First** - Recommendation algorithms are the project's main value
2. **Test Edge Cases** - Empty inputs, invalid data, boundary conditions
3. **Test Business Logic** - Ensure algorithms work as expected
4. **Test Security** - Password hashing and verification
5. **Test Infrastructure** - Database setup and connections

## 📝 Adding New Tests

When adding new features, create corresponding tests:

1. Create test class inheriting from `unittest.TestCase`
2. Use `setUp()` for test data preparation
3. Use `tearDown()` for cleanup
4. Name test methods with `test_` prefix
5. Use descriptive assertions with messages

Example:
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        # Prepare test data
        pass
    
    def test_feature_works_correctly(self):
        # Test implementation
        result = new_function()
        self.assertEqual(result, expected_value,
                        "Feature should work correctly")
    
    def tearDown(self):
        # Cleanup
        pass
```

## ✅ Policy Compliance

This test suite demonstrates:
- ✅ **Testing Phase** - Formal automated tests
- ✅ **Algorithm Validation** - Tests prove algorithms work correctly
- ✅ **Software Engineering Practice** - Industry-standard testing approach
- ✅ **Code Quality Assurance** - Catches bugs before production

## 🔍 Test Requirements Met

According to project policy:
> "The project should be practiced by following analysis, design, implementation and **testing phases**."

✅ **This test suite fulfills the testing phase requirement**

---

**Last Updated:** 2024
**Test Framework:** Python unittest
**Total Test Cases:** 37+
