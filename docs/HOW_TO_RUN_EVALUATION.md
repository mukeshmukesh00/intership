# How to Run Offline Evaluation - Quick Start Guide

## Prerequisites

1. **Database**: Make sure `internship.db` exists in the project root
2. **Data**: You need some application data (students who applied to internships) for evaluation
3. **Python**: Python 3.7+ installed

## Quick Start

### Step 1: Check Your Database

First, verify your database exists and has data:

```bash
# On Windows (PowerShell)
python -c "import sqlite3; conn = sqlite3.connect('internship.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM applications'); print(f'Applications: {cursor.fetchone()[0]}')"
```

Or check manually:
- The database file should be at: `internship.db` (in project root)
- It should have data in the `applications` table (this is used as ground truth)

### Step 2: Run Basic Evaluation

```bash
python offline_evaluation.py
```

This will:
- Load data from `internship.db`
- Evaluate all three algorithms (Content-Based, Collaborative, Hybrid)
- Generate a report in `evaluation_report.json`
- Print results to console

### Step 3: View Results

After running, you'll see:
1. **Console Output**: Formatted evaluation report
2. **JSON File**: `evaluation_report.json` with detailed results

## Common Usage Examples

### Example 1: Basic Evaluation

```bash
python offline_evaluation.py
```

**Output:**
- Console: Formatted evaluation report
- File: `evaluation_report.json`

### Example 2: Custom K Values

```bash
python offline_evaluation.py --k 5 10 20 50
```

Evaluates at K=5, K=10, K=20, and K=50.

### Example 3: Custom Database Path

```bash
python offline_evaluation.py --db path/to/your/database.db
```

### Example 4: Run Validation First

```bash
python offline_evaluation.py --validate
```

Validates algorithms before running evaluation (checks if data is sufficient).

### Example 5: Run A/B Testing

```bash
python offline_evaluation.py --ab-test
```

Splits users into two groups and compares algorithms.

### Example 6: All Options Combined

```bash
python offline_evaluation.py --db internship.db --k 5 10 20 --output my_report.json --ab-test --validate
```

## Understanding the Output

### Console Output

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
...
```

### JSON Report Structure

The `evaluation_report.json` file contains:

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
  "comparison": { ... },
  "summary": { ... }
}
```

## Programmatic Usage

You can also use the evaluation programmatically:

```python
from offline_evaluation import run_comprehensive_evaluation

# Run evaluation
report = run_comprehensive_evaluation(
    db_path="internship.db",
    k_values=[5, 10, 20],
    output_file="evaluation_report.json",
    ab_test=False
)

# Access results
print(f"Content-Based Precision@5: {report['algorithms']['content_based']['precision'][5]}")
print(f"Hybrid Precision@5: {report['algorithms']['hybrid']['precision'][5]}")
```

## Troubleshooting

### Problem: "Database file not found"

**Solution:**
- Make sure `internship.db` exists in the project root
- Or specify the path: `python offline_evaluation.py --db path/to/database.db`

### Problem: "No users with application history found"

**Solution:**
- You need users who have applied to internships (this is the ground truth)
- Make sure the `applications` table has data
- Run validation first: `python offline_evaluation.py --validate`

### Problem: "Error evaluating [algorithm] for user X"

**Solution:**
- Some users might not have the required data (e.g., no skills for Content-Based)
- This is normal - the evaluation skips users without sufficient data
- Check the validation output to see data coverage

### Problem: "Low metrics" (all scores are very low)

**Possible Causes:**
- Insufficient data
- Algorithm parameters need tuning
- Data quality issues

**Solution:**
- Run validation: `python offline_evaluation.py --validate`
- Check if users have skills (Content-Based)
- Check if users have application history (Collaborative)
- Ensure internships have required skills

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--db` | Database file path | `internship.db` |
| `--k` | K values for evaluation | `5 10 20` |
| `--output` | Output JSON file path | `evaluation_report.json` |
| `--ab-test` | Run A/B testing | `False` |
| `--validate` | Run algorithm validation | `False` |

## Examples with Expected Output

### Example 1: First Time Running

```bash
# Step 1: Validate first
python offline_evaluation.py --validate
```

**Expected Output:**
```
================================================================================
ALGORITHM-SPECIFIC VALIDATION
================================================================================

Content-Based Algorithm Validation:
{
  "users_with_skills": 45,
  "internships_with_skills": 30,
  "coverage": true
}

Collaborative Filtering Algorithm Validation:
{
  "total_students": 50,
  "users_with_applications": 30,
  "cold_start_users": 20,
  "sparsity": 0.95,
  "average_applications_per_user": 7.8
}

Hybrid Algorithm Validation:
{
  "content_based": { ... },
  "collaborative_filtering": { ... },
  "hybrid_ready": true
}
```

```bash
# Step 2: Run evaluation
python offline_evaluation.py
```

### Example 2: Quick Evaluation

```bash
python offline_evaluation.py --k 5 10
```

Quick evaluation at only K=5 and K=10.

### Example 3: Full Evaluation with A/B Testing

```bash
python offline_evaluation.py --k 5 10 20 --ab-test --output full_report.json
```

## Next Steps

After running evaluation:

1. **Review the Report**: Check `evaluation_report.json` for detailed results
2. **Compare Algorithms**: See which algorithm performs best for each metric
3. **Check Recommendations**: Review the summary recommendations
4. **Tune Parameters**: Adjust algorithm parameters if needed
5. **Run A/B Testing**: Test algorithms in production-like scenarios

## Additional Resources

- **Full Documentation**: See `docs/OFFLINE_EVALUATION_GUIDE.md`
- **Implementation Details**: See `docs/OFFLINE_EVALUATION_IMPLEMENTATION.md`
- **Examples**: See `example_evaluation.py`

## Quick Reference

```bash
# Basic evaluation
python offline_evaluation.py

# With validation
python offline_evaluation.py --validate

# With A/B testing
python offline_evaluation.py --ab-test

# Custom options
python offline_evaluation.py --db internship.db --k 5 10 20 --output report.json

# Help (if needed)
python offline_evaluation.py --help
```

## Notes

- Evaluation requires ground truth data (applications table)
- More data = more reliable evaluation
- Evaluation can take a few minutes with large datasets
- Results are saved to JSON file for further analysis

