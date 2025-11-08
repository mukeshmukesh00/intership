# example_evaluation.py - Example usage of offline evaluation system
"""
Example script demonstrating how to use the offline evaluation system.
"""

from offline_evaluation import (
    run_comprehensive_evaluation,
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_ndcg,
    ABTest,
    validate_content_based_algorithm,
    validate_collaborative_filtering_algorithm,
    validate_hybrid_algorithm
)
import sqlite3
import json

def example_basic_metrics():
    """Example: Calculate basic metrics manually."""
    print("="*80)
    print("EXAMPLE: Basic Metrics Calculation")
    print("="*80)
    
    # Simulated data
    recommended_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    relevant_list = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    k = 10
    
    # Calculate metrics
    precision = calculate_precision_at_k(recommended_list, relevant_list, k)
    recall = calculate_recall_at_k(recommended_list, relevant_list, k)
    ndcg = calculate_ndcg(recommended_list, relevant_list, k)
    
    print(f"\nRecommended items (top-{k}): {recommended_list}")
    print(f"Relevant items: {relevant_list}")
    print(f"\nPrecision@{k}: {precision:.4f}")
    print(f"Recall@{k}: {recall:.4f}")
    print(f"NDCG@{k}: {ndcg:.4f}")
    print()


def example_validation(db_path="internship.db"):
    """Example: Validate algorithms before evaluation."""
    print("="*80)
    print("EXAMPLE: Algorithm Validation")
    print("="*80)
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Validate Content-Based
        print("\n1. Content-Based Algorithm Validation:")
        content_val = validate_content_based_algorithm(conn)
        print(f"   Users with skills: {content_val['users_with_skills']}")
        print(f"   Internships with skills: {content_val['internships_with_skills']}")
        print(f"   Coverage: {'✓' if content_val['coverage'] else '✗'}")
        
        # Validate Collaborative Filtering
        print("\n2. Collaborative Filtering Algorithm Validation:")
        collab_val = validate_collaborative_filtering_algorithm(conn)
        print(f"   Total students: {collab_val['total_students']}")
        print(f"   Users with applications: {collab_val['users_with_applications']}")
        print(f"   Cold start users: {collab_val['cold_start_users']}")
        print(f"   Sparsity: {collab_val['sparsity']:.2%}")
        print(f"   Average applications per user: {collab_val['average_applications_per_user']:.2f}")
        
        # Validate Hybrid
        print("\n3. Hybrid Algorithm Validation:")
        hybrid_val = validate_hybrid_algorithm(conn)
        print(f"   Hybrid ready: {'✓' if hybrid_val['hybrid_ready'] else '✗'}")
        
        conn.close()
        print()
        
    except FileNotFoundError:
        print(f"   Database not found at {db_path}")
        print("   Please ensure the database exists before running evaluation.\n")
    except Exception as e:
        print(f"   Error: {e}\n")


def example_comprehensive_evaluation(db_path="internship.db"):
    """Example: Run comprehensive evaluation."""
    print("="*80)
    print("EXAMPLE: Comprehensive Evaluation")
    print("="*80)
    
    try:
        # Run evaluation
        report = run_comprehensive_evaluation(
            db_path=db_path,
            k_values=[5, 10, 20],
            output_file="evaluation_report.json",
            ab_test=False
        )
        
        if report:
            print("\n✓ Evaluation completed successfully!")
            print(f"  Report saved to: evaluation_report.json")
        else:
            print("\n✗ Evaluation failed or no data available")
        print()
        
    except FileNotFoundError:
        print(f"\n✗ Database not found at {db_path}")
        print("  Please ensure the database exists before running evaluation.\n")
    except Exception as e:
        print(f"\n✗ Error during evaluation: {e}\n")


def example_ab_testing(db_path="internship.db"):
    """Example: Run A/B testing."""
    print("="*80)
    print("EXAMPLE: A/B Testing")
    print("="*80)
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Get user IDs from applications
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT student_id FROM applications")
        user_ids = [row['student_id'] for row in cursor.fetchall()]
        
        if len(user_ids) < 4:
            print(f"\n✗ Not enough users for A/B testing (need at least 4, found {len(user_ids)})")
            conn.close()
            return
        
        # Create A/B test
        ab_test = ABTest(
            conn=conn,
            group_a_algorithm='content',
            group_b_algorithm='hybrid'
        )
        
        # Split users
        ab_test.split_users(user_ids, split_ratio=0.5, random_seed=42)
        
        # Run A/B test
        results = ab_test.run_ab_test(k_values=[5, 10])
        
        # Print results
        print("\nA/B Test Results:")
        print(json.dumps(results, indent=2))
        
        conn.close()
        print()
        
    except FileNotFoundError:
        print(f"\n✗ Database not found at {db_path}")
        print("  Please ensure the database exists before running evaluation.\n")
    except Exception as e:
        print(f"\n✗ Error during A/B testing: {e}\n")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("OFFLINE EVALUATION EXAMPLES")
    print("="*80 + "\n")
    
    # Example 1: Basic metrics
    example_basic_metrics()
    
    # Example 2: Validation
    example_validation()
    
    # Example 3: Comprehensive evaluation
    # Uncomment to run (requires database with data)
    # example_comprehensive_evaluation()
    
    # Example 4: A/B testing
    # Uncomment to run (requires database with data)
    # example_ab_testing()
    
    print("="*80)
    print("EXAMPLES COMPLETE")
    print("="*80)
    print("\nTo run full evaluation, use:")
    print("  python offline_evaluation.py")
    print("\nOr programmatically:")
    print("  from offline_evaluation import run_comprehensive_evaluation")
    print("  report = run_comprehensive_evaluation()")
    print()


if __name__ == "__main__":
    main()



