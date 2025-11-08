# Offline Evaluation System - README

## Quick Start

### Run Evaluation (Easiest Way)

```bash
python offline_evaluation.py
```

This will:
1. Load data from `internship.db`
2. Evaluate all three algorithms
3. Generate `evaluation_report.json`
4. Print results to console

### Run with Validation

```bash
python offline_evaluation.py --validate
```

### Run with A/B Testing

```bash
python offline_evaluation.py --ab-test
```

## What You Get

### 1. Console Output
Formatted evaluation report showing:
- Precision@K for each algorithm
- Recall@K for each algorithm  
- NDCG@K for each algorithm
- MAP@K for each algorithm
- Best performing algorithm for each metric

### 2. JSON Report
Detailed results saved to `evaluation_report.json`:
- All metrics for all algorithms
- Comparison tables
- Summary and recommendations

## Example Output

```
================================================================================
COMPREHENSIVE EVALUATION REPORT
================================================================================

PRECISION:
--------------------------------------------------------------------------------
K          Content-Based        Collaborative        Hybrid               Best           
--------------------------------------------------------------------------------
5          0.4500               0.3800               0.5200               hybrid        
10         0.3800               0.3500               0.4800               hybrid        
20         0.3200               0.3000               0.4200               hybrid        
```

## Documentation

- **[How to Run Evaluation](./HOW_TO_RUN_EVALUATION.md)** - Step-by-step guide
- **[Evaluation Guide](./OFFLINE_EVALUATION_GUIDE.md)** - Comprehensive documentation
- **[Implementation Details](./OFFLINE_EVALUATION_IMPLEMENTATION.md)** - Technical details

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--db` | Database path | `--db internship.db` |
| `--k` | K values | `--k 5 10 20` |
| `--output` | Output file | `--output report.json` |
| `--ab-test` | Run A/B test | `--ab-test` |
| `--validate` | Validate algorithms | `--validate` |

## Requirements

- Python 3.7+
- Database: `internship.db` (with application data)
- No additional dependencies

## Metrics Explained

- **Precision@K**: Accuracy of top-K recommendations
- **Recall@K**: Coverage of relevant items
- **NDCG@K**: Ranking quality considering position
- **MAP@K**: Average precision across users

## Algorithms Compared

1. **Content-Based Filtering** - Skill matching
2. **Collaborative Filtering** - User similarity
3. **Hybrid Approach** - Combination of both

## Need Help?

See the [How to Run Evaluation](./HOW_TO_RUN_EVALUATION.md) guide for:
- Troubleshooting
- Detailed examples
- Understanding output
- Programmatic usage

## Quick Examples

```bash
# Basic evaluation
python offline_evaluation.py

# Custom K values
python offline_evaluation.py --k 5 10 20 50

# With validation
python offline_evaluation.py --validate

# With A/B testing
python offline_evaluation.py --ab-test

# All options
python offline_evaluation.py --db internship.db --k 5 10 20 --output report.json --ab-test --validate
```



