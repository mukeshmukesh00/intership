# Evaluation Quick Start

## How to Run Evaluation

### Option 1: Simple Run (Recommended)

```bash
python offline_evaluation.py
```

**Output:**
- Console: Formatted evaluation report
- File: `evaluation_report.json`

### Option 2: With Validation

```bash
python offline_evaluation.py --validate
```

Validates algorithms before evaluation.

### Option 3: With A/B Testing

```bash
python offline_evaluation.py --ab-test
```

Compares algorithms using A/B testing.

## What You'll See

### Console Output Example

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
```

### JSON Report

Saved to `evaluation_report.json` with detailed metrics for:
- Content-Based Filtering
- Collaborative Filtering  
- Hybrid Approach

## Requirements

- Database: `internship.db` (must exist)
- Data: Users who applied to internships (ground truth)
- Python: 3.7+

## Common Commands

```bash
# Basic evaluation
python offline_evaluation.py

# Custom K values
python offline_evaluation.py --k 5 10 20

# Custom database
python offline_evaluation.py --db your_database.db

# Custom output file
python offline_evaluation.py --output my_report.json

# All options
python offline_evaluation.py --db internship.db --k 5 10 20 --output report.json --validate
```

## Documentation

Full documentation in `docs/` folder:
- `docs/HOW_TO_RUN_EVALUATION.md` - Detailed guide
- `docs/OFFLINE_EVALUATION_GUIDE.md` - Complete documentation
- `docs/EVALUATION_README.md` - Quick reference

## Troubleshooting

**Problem: Database not found**
- Make sure `internship.db` exists in project root
- Or use: `python offline_evaluation.py --db path/to/db.db`

**Problem: No applications found**
- You need users who applied to internships
- Run Flask app first to create sample data

**Problem: Low metrics**
- Normal with limited data
- More applications = better evaluation

## Help

```bash
python offline_evaluation.py --help
```

For detailed help, see: `docs/HOW_TO_RUN_EVALUATION.md`

