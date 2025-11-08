# Offline Evaluation Guide - Internship Recommendation System

## Overview

This guide explains how to use the comprehensive offline evaluation system to compare Content-Based Filtering, Collaborative Filtering, and Hybrid recommendation algorithms.

## Features

### **Offline Evaluation Metrics:**
1. **Precision@K**: Fraction of top-K recommendations that are relevant
2. **Recall@K**: Fraction of relevant items found in top-K
3. **Mean Average Precision (MAP)**: Average precision across multiple users
4. **Normalized Discounted Cumulative Gain (NDCG)**: Accounts for ranking position of relevant items

### **Online Evaluation Support:**
- A/B Testing framework
- User survey data collection
- Algorithm-specific validation
- Comprehensive evaluation reports

## Installation

No additional dependencies required. The evaluation script uses the same dependencies as the main application.

## Usage

### Basic Usage

Run the comprehensive evaluation:

```bash
python offline_evaluation.py
```

### Advanced Usage

```bash
# Specify database path and K values
python offline_evaluation.py --db internship.db --k 5 10 20

# Run A/B testing
python offline_evaluation.py --ab-test

# Run algorithm-specific validation
python offline_evaluation.py --validate

# Save report to custom file
python offline_evaluation.py --output my_report.json
```

### Command Line Arguments

- `--db`: Path to database file (default: `internship.db`)
- `--k`: K values for evaluation (default: `5 10 20`)
- `--output`: Output file for JSON report (default: `evaluation_report.json`)
- `--ab-test`: Run A/B testing
- `--validate`: Run algorithm-specific validation

## Programmatic Usage

### Running Comprehensive Evaluation

```python
from offline_evaluation import run_comprehensive_evaluation

# Run evaluation
report = run_comprehensive_evaluation(
    db_path="internship.db",
    k_values=[5, 10, 20],
    output_file="evaluation_report.json",
    ab_test=True
)
```

### Calculating Individual Metrics

```python
from offline_evaluation import (
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_ndcg,
    calculate_map
)

# Example: Calculate Precision@10
recommended = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
relevant = [2, 4, 6, 8, 10]
precision = calculate_precision_at_k(recommended, relevant, k=10)

# Example: Calculate Recall@10
recall = calculate_recall_at_k(recommended, relevant, k=10)

# Example: Calculate NDCG@10
ndcg = calculate_ndcg(recommended, relevant, k=10)
```

### A/B Testing

```python
from offline_evaluation import ABTest
import sqlite3

# Connect to database
conn = sqlite3.connect("internship.db")
conn.row_factory = sqlite3.Row

# Create A/B test
ab_test = ABTest(
    conn=conn,
    group_a_algorithm='content',
    group_b_algorithm='hybrid'
)

# Get user IDs
user_ids = [1, 2, 3, 4, 5, ...]  # Your user IDs

# Split users (50/50 by default)
ab_test.split_users(user_ids, split_ratio=0.5, random_seed=42)

# Run A/B test
results = ab_test.run_ab_test(k_values=[5, 10, 20])
```

### Algorithm Validation

```python
from offline_evaluation import (
    validate_content_based_algorithm,
    validate_collaborative_filtering_algorithm,
    validate_hybrid_algorithm
)
import sqlite3

conn = sqlite3.connect("internship.db")
conn.row_factory = sqlite3.Row

# Validate Content-Based algorithm
content_val = validate_content_based_algorithm(conn)
print(f"Users with skills: {content_val['users_with_skills']}")
print(f"Internships with skills: {content_val['internships_with_skills']}")

# Validate Collaborative Filtering algorithm
collab_val = validate_collaborative_filtering_algorithm(conn)
print(f"Sparsity: {collab_val['sparsity']:.2%}")
print(f"Cold start users: {collab_val['cold_start_users']}")

# Validate Hybrid algorithm
hybrid_val = validate_hybrid_algorithm(conn)
print(f"Hybrid ready: {hybrid_val['hybrid_ready']}")
```

## Understanding the Metrics

### Precision@K

**Definition**: Fraction of top-K recommendations that are relevant.

**Formula**: `Precision@K = |{relevant items in top-K}| / K`

**Interpretation**: 
- Higher is better (0.0 to 1.0)
- Measures accuracy of recommendations
- Example: If 3 out of 5 recommendations are relevant, Precision@5 = 0.6

### Recall@K

**Definition**: Fraction of relevant items found in top-K.

**Formula**: `Recall@K = |{relevant items in top-K}| / |{all relevant items}|`

**Interpretation**:
- Higher is better (0.0 to 1.0)
- Measures coverage of relevant items
- Example: If user has 10 relevant items and we find 7 in top-10, Recall@10 = 0.7

### Mean Average Precision (MAP)

**Definition**: Average precision across all users.

**Formula**: `MAP@K = (1/|U|) * Σ AP@K(u) for all users u`

**Interpretation**:
- Higher is better (0.0 to 1.0)
- Considers ranking order of relevant items
- More sophisticated than precision/recall

### Normalized Discounted Cumulative Gain (NDCG)

**Definition**: Accounts for ranking position of relevant items.

**Formula**: `NDCG@K = DCG@K / IDCG@K`

**Interpretation**:
- Higher is better (0.0 to 1.0)
- Rewards placing relevant items higher in ranking
- Best metric for ranking quality

## Evaluation Report

The evaluation generates a comprehensive JSON report with:

1. **Timestamp**: When the evaluation was run
2. **Algorithm Results**: Metrics for each algorithm (Content-Based, Collaborative, Hybrid)
3. **Comparison**: Side-by-side comparison of all algorithms
4. **Summary**: Best performing algorithm for each metric
5. **Recommendations**: Actionable insights

### Report Structure

```json
{
  "timestamp": "2025-01-15T10:30:00",
  "algorithms": {
    "content_based": {
      "precision": {"5": 0.45, "10": 0.38, "20": 0.32},
      "recall": {"5": 0.25, "10": 0.42, "20": 0.58},
      "ndcg": {"5": 0.52, "10": 0.48, "20": 0.44},
      "map": {"5": 0.35, "10": 0.42, "20": 0.48}
    },
    "collaborative_filtering": { ... },
    "hybrid": { ... }
  },
  "comparison": {
    "precision": {
      "5": {
        "content_based": 0.45,
        "collaborative_filtering": 0.38,
        "hybrid": 0.52,
        "best_algorithm": "hybrid"
      }
    }
  },
  "summary": {
    "best_overall": { ... },
    "recommendations": [ ... ]
  }
}
```

## A/B Testing

A/B testing allows you to compare two algorithms by splitting users into two groups:

1. **Group A**: Users receive recommendations from Algorithm A
2. **Group B**: Users receive recommendations from Algorithm B

### When to Use A/B Testing

- Compare new algorithm against existing one
- Test algorithm improvements
- Measure real-world performance differences

### A/B Test Results

The A/B test returns:
- Metrics for Group A
- Metrics for Group B
- Comparison of performance
- Statistical significance (if applicable)

## Algorithm-Specific Validation

### Content-Based Validation

Checks:
- Number of users with skills in profile
- Number of internships with required skills
- Coverage (whether algorithm can work)

### Collaborative Filtering Validation

Checks:
- Application sparsity (how sparse is the user-item matrix)
- Cold start users (users with no applications)
- Average applications per user

### Hybrid Validation

Checks:
- Whether both algorithms are ready
- Overall system readiness

## Best Practices

1. **Use Multiple K Values**: Evaluate at different K values (5, 10, 20) to understand performance at different recommendation list sizes.

2. **Ensure Sufficient Data**: Make sure you have enough ground truth data (applications) for meaningful evaluation.

3. **Run Regular Evaluations**: Evaluate periodically as your data grows and algorithms improve.

4. **Compare All Metrics**: Don't rely on a single metric. Look at precision, recall, NDCG, and MAP together.

5. **Validate Algorithms First**: Run validation before evaluation to ensure algorithms can work with your data.

6. **Use A/B Testing**: For production systems, use A/B testing to compare algorithms in real-world scenarios.

## Troubleshooting

### No Users with Application History

**Problem**: Evaluation requires ground truth data (applications).

**Solution**: 
- Ensure users have applied to internships
- Check that applications table has data
- Use validation to check data availability

### Algorithm Returns No Recommendations

**Problem**: Algorithm returns empty list for some users.

**Solution**:
- Check if users have skills (Content-Based)
- Check if users have application history (Collaborative)
- Validate algorithms before evaluation

### Low Metrics

**Problem**: All metrics are very low.

**Possible Causes**:
- Insufficient data
- Algorithm parameters need tuning
- Data quality issues

**Solution**:
- Validate algorithms
- Check data quality
- Adjust algorithm parameters (e.g., similarity thresholds)

## Example Output

```
================================================================================
OFFLINE EVALUATION - INTERNSHIP RECOMMENDATION SYSTEM
================================================================================
Database: internship.db
K values: [5, 10, 20]
Timestamp: 2025-01-15T10:30:00

Loading ground truth data...
Found 50 users with application history
Total applications: 234

Evaluating Content-Based Filtering...
Evaluating Collaborative Filtering...
Evaluating Hybrid Approach...

Generating evaluation report...

================================================================================
COMPREHENSIVE EVALUATION REPORT
================================================================================
Generated at: 2025-01-15T10:30:00

PRECISION:
--------------------------------------------------------------------------------
K          Content-Based        Collaborative          Hybrid              Best          
--------------------------------------------------------------------------------
5          0.4500               0.3800                 0.5200               hybrid        
10         0.3800               0.3500                 0.4800               hybrid        
20         0.3200               0.3000                 0.4200               hybrid        

RECALL:
--------------------------------------------------------------------------------
K          Content-Based        Collaborative          Hybrid              Best          
--------------------------------------------------------------------------------
5          0.2500               0.2200                 0.3200               hybrid        
10         0.4200               0.3800                 0.5500               hybrid        
20         0.5800               0.5200                 0.6800               hybrid        

...

Evaluation report saved to: evaluation_report.json

================================================================================
EVALUATION COMPLETE
================================================================================
```

## Additional Resources

- [Algorithm Documentation](./ALGORITHM_UPDATE_SUMMARY.md)
- [Database Schema](./DATABASE_INFORMATION.md)
- [Testing Guide](./TESTING_PHASE_EXPLANATION.md)



