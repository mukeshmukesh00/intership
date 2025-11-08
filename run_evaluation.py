# run_evaluation.py - Simple script to run evaluation with better output handling
"""
Simple wrapper script to run offline evaluation with better error handling.
"""

import sys
import os

def main():
    print("="*80)
    print("OFFLINE EVALUATION RUNNER")
    print("="*80)
    print()
    
    # Check if database exists
    db_path = "internship.db"
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        print(f"Please ensure the database exists in the project root.")
        print()
        print("You can:")
        print("  1. Run the Flask app first to create the database")
        print("  2. Or specify a different database path: python offline_evaluation.py --db your_db.db")
        return 1
    
    print(f"Database found: {db_path}")
    
    # Check database has data
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check applications table
        cursor.execute("SELECT COUNT(*) FROM applications")
        app_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT student_id) FROM applications")
        user_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"Applications in database: {app_count}")
        print(f"Users with applications: {user_count}")
        print()
        
        if app_count == 0:
            print("WARNING: No applications found in database.")
            print("Evaluation requires application data (ground truth).")
            print()
            print("You need:")
            print("  - Students who have applied to internships")
            print("  - Data in the 'applications' table")
            print()
            print("To generate sample data:")
            print("  1. Run the Flask app: python app_new.py")
            print("  2. Register users and create applications")
            print("  3. Then run evaluation again")
            return 1
        
        if user_count < 2:
            print("WARNING: Not enough users for meaningful evaluation.")
            print(f"Found {user_count} users, but need at least 2-3 users.")
        
    except Exception as e:
        print(f"ERROR checking database: {e}")
        return 1
    
    # Run evaluation
    print("Running evaluation...")
    print("="*80)
    print()
    
    try:
        from offline_evaluation import run_comprehensive_evaluation
        
        report = run_comprehensive_evaluation(
            db_path=db_path,
            k_values=[5, 10, 20],
            output_file="evaluation_report.json",
            ab_test=False
        )
        
        if report:
            print()
            print("="*80)
            print("EVALUATION COMPLETE!")
            print("="*80)
            print()
            print("Results saved to: evaluation_report.json")
            print()
            print("To view results:")
            print("  1. Check the console output above")
            print("  2. Open evaluation_report.json in a text editor")
            print("  3. Or use: python -c \"import json; print(json.dump(open('evaluation_report.json').read(), indent=2))\"")
            return 0
        else:
            print("Evaluation completed but returned no results.")
            return 1
            
    except ImportError as e:
        print(f"ERROR: Could not import evaluation module: {e}")
        print("Make sure offline_evaluation.py is in the project root.")
        return 1
    except Exception as e:
        print(f"ERROR during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())



