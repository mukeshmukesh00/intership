# offline_evaluation.py - Comprehensive Offline Evaluation for Internship Recommendation System
"""
This module provides comprehensive offline evaluation metrics for comparing
Content-Based Filtering, Collaborative Filtering, and Hybrid recommendation algorithms.

Metrics Implemented:
- Precision@K: Fraction of top-K recommendations that are relevant
- Recall@K: Fraction of relevant items found in top-K
- Mean Average Precision (MAP): Average precision across all users
- Normalized Discounted Cumulative Gain (NDCG): Accounts for ranking position

Online Evaluation Support:
- A/B Testing framework
- User survey data collection
- Algorithm-specific validation
- Comprehensive evaluation reports
"""

import sqlite3
import math
import json
import os
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
from collections import defaultdict
import sys

# Add utils to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.recommendations import (
    content_based_recommendations,
    collaborative_filtering
)


# ============================================================================
# CORE EVALUATION METRICS
# ============================================================================

def calculate_precision_at_k(recommended_list: List[int], relevant_list: List[int], k: int) -> float:
    """
    Calculate Precision@K - fraction of top-K recommendations that are relevant.
    
    Args:
        recommended_list: List of recommended item IDs (sorted by relevance)
        relevant_list: List of relevant item IDs (ground truth)
        k: Number of top recommendations to consider
    
    Returns:
        Precision@K score (0.0 to 1.0)
    
    Formula:
        Precision@K = |{relevant items in top-K}| / K
    """
    if k == 0:
        return 0.0
    
    # Take top k recommendations
    top_k = recommended_list[:k]
    
    # Count how many are relevant
    relevant_in_top_k = len(set(top_k) & set(relevant_list))
    
    # Precision = relevant items in top-k / k
    precision = relevant_in_top_k / k if k > 0 else 0.0
    
    return precision


def calculate_recall_at_k(recommended_list: List[int], relevant_list: List[int], k: int) -> float:
    """
    Calculate Recall@K - fraction of relevant items found in top-K.
    
    Args:
        recommended_list: List of recommended item IDs (sorted by relevance)
        relevant_list: List of relevant item IDs (ground truth)
        k: Number of top recommendations to consider
    
    Returns:
        Recall@K score (0.0 to 1.0)
    
    Formula:
        Recall@K = |{relevant items in top-K}| / |{all relevant items}|
    """
    if not relevant_list:
        return 0.0
    
    if k == 0:
        return 0.0
    
    # Take top k recommendations
    top_k = recommended_list[:k]
    
    # Count how many relevant items are in top-k
    relevant_in_top_k = len(set(top_k) & set(relevant_list))
    
    # Recall = relevant items in top-k / total relevant items
    recall = relevant_in_top_k / len(relevant_list) if relevant_list else 0.0
    
    return recall


def calculate_average_precision(recommended_list: List[int], relevant_list: Set[int], k: int) -> float:
    """
    Calculate Average Precision (AP) for a single user.
    
    Args:
        recommended_list: List of recommended item IDs (sorted by relevance)
        relevant_list: Set of relevant item IDs (ground truth)
        k: Number of top recommendations to consider
    
    Returns:
        Average Precision score (0.0 to 1.0)
    
    Formula:
        AP = (1/|R|) * Σ(Precision@i * rel(i))
        where rel(i) = 1 if item at position i is relevant, else 0
    """
    if not relevant_list:
        return 0.0
    
    if k == 0:
        return 0.0
    
    top_k = recommended_list[:k]
    relevant_count = 0
    precision_sum = 0.0
    
    for i, item in enumerate(top_k, 1):
        if item in relevant_list:
            relevant_count += 1
            precision_at_i = relevant_count / i
            precision_sum += precision_at_i
    
    # Average Precision = sum of precisions / total relevant items
    ap = precision_sum / len(relevant_list) if relevant_list else 0.0
    
    return ap


def calculate_map(recommendations: Dict[int, List[int]], ground_truth: Dict[int, List[int]], k_values: List[int] = [5, 10]) -> Dict[int, float]:
    """
    Calculate Mean Average Precision (MAP) across multiple users.
    
    Args:
        recommendations: Dictionary mapping user_id to list of recommended item IDs
        ground_truth: Dictionary mapping user_id to list of relevant item IDs
        k_values: List of K values to evaluate (e.g., [5, 10, 20])
    
    Returns:
        Dictionary mapping K to MAP@K score
    
    Formula:
        MAP@K = (1/|U|) * Σ AP@K(u) for all users u
    """
    map_scores = {}
    
    for k in k_values:
        ap_scores = []
        
        # Calculate AP for each user
        for user_id, recommended_list in recommendations.items():
            if user_id in ground_truth:
                relevant_list = set(ground_truth[user_id])
                if relevant_list:  # Only calculate if user has relevant items
                    ap = calculate_average_precision(recommended_list, relevant_list, k)
                    ap_scores.append(ap)
        
        # MAP = mean of all AP scores
        map_scores[k] = sum(ap_scores) / len(ap_scores) if ap_scores else 0.0
    
    return map_scores


def calculate_dcg(recommended_list: List[int], relevant_list: Set[int], k: int) -> float:
    """
    Calculate Discounted Cumulative Gain (DCG).
    
    Args:
        recommended_list: List of recommended item IDs (sorted by relevance)
        relevant_list: Set of relevant item IDs (ground truth)
        k: Number of top recommendations to consider
    
    Returns:
        DCG score
    """
    dcg = 0.0
    top_k = recommended_list[:k]
    
    for i, item in enumerate(top_k, 1):
        if item in relevant_list:
            # DCG: rel_i / log2(i + 1)
            # Using binary relevance (1 if relevant, 0 otherwise)
            relevance = 1.0
            dcg += relevance / math.log2(i + 1)
    
    return dcg


def calculate_ndcg(recommended_list: List[int], relevant_list: List[int], k: int) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain (NDCG).
    Accounts for ranking position of relevant items.
    
    Args:
        recommended_list: List of recommended item IDs (sorted by relevance)
        relevant_list: List of relevant item IDs (ground truth)
        k: Number of top recommendations to consider
    
    Returns:
        NDCG@K score (0.0 to 1.0)
    
    Formula:
        NDCG@K = DCG@K / IDCG@K
        where IDCG@K is the ideal DCG (perfect ranking)
    """
    if not relevant_list:
        return 0.0
    
    if k == 0:
        return 0.0
    
    relevant_set = set(relevant_list)
    
    # Calculate DCG for recommended list
    dcg = calculate_dcg(recommended_list, relevant_set, k)
    
    # Calculate Ideal DCG (IDCG) - perfect ranking
    # Sort relevant items by their ideal order (all relevant items first)
    ideal_list = list(relevant_set)[:k]
    idcg = calculate_dcg(ideal_list, relevant_set, k)
    
    # NDCG = DCG / IDCG
    ndcg = dcg / idcg if idcg > 0 else 0.0
    
    return ndcg


# ============================================================================
# ALGORITHM EVALUATION FUNCTIONS
# ============================================================================

def get_ground_truth(conn: sqlite3.Connection, user_ids: Optional[List[int]] = None) -> Dict[int, List[int]]:
    """
    Get ground truth data from applications table.
    
    Args:
        conn: Database connection
        user_ids: Optional list of user IDs to filter (None = all users)
    
    Returns:
        Dictionary mapping user_id to list of applied internship IDs
    """
    cursor = conn.cursor()
    
    if user_ids:
        placeholders = ','.join('?' * len(user_ids))
        query = f"SELECT student_id, internship_id FROM applications WHERE student_id IN ({placeholders})"
        cursor.execute(query, user_ids)
    else:
        cursor.execute("SELECT student_id, internship_id FROM applications")
    
    applications = cursor.fetchall()
    
    ground_truth = defaultdict(list)
    for app in applications:
        user_id = app['student_id']
        internship_id = app['internship_id']
        ground_truth[user_id].append(internship_id)
    
    return dict(ground_truth)


def evaluate_content_based(
    conn: sqlite3.Connection,
    user_ids: List[int],
    ground_truth: Dict[int, List[int]],
    k_values: List[int] = [5, 10, 20]
) -> Dict[str, Dict[int, float]]:
    """
    Evaluate Content-Based Filtering algorithm.
    
    Returns:
        Dictionary with metrics: {'precision': {k: score}, 'recall': {k: score}, ...}
    """
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    
    results = {
        'precision': defaultdict(list),
        'recall': defaultdict(list),
        'ndcg': defaultdict(list),
        'map': {}
    }
    
    recommendations = {}
    
    for user_id in user_ids:
        if user_id not in ground_truth:
            continue
        
        # Get content-based recommendations
        try:
            recs = content_based_recommendations(user_id, cursor)
            recommended_ids = [rec['id'] for rec in recs]
            recommendations[user_id] = recommended_ids
            
            relevant_ids = ground_truth[user_id]
            
            # Calculate metrics for each k
            for k in k_values:
                precision = calculate_precision_at_k(recommended_ids, relevant_ids, k)
                recall = calculate_recall_at_k(recommended_ids, relevant_ids, k)
                ndcg = calculate_ndcg(recommended_ids, relevant_ids, k)
                
                results['precision'][k].append(precision)
                results['recall'][k].append(recall)
                results['ndcg'][k].append(ndcg)
        except Exception as e:
            print(f"Error evaluating content-based for user {user_id}: {e}")
            continue
    
    # Calculate MAP
    results['map'] = calculate_map(recommendations, ground_truth, k_values)
    
    # Average metrics across users
    final_results = {}
    for metric in ['precision', 'recall', 'ndcg']:
        final_results[metric] = {}
        for k in k_values:
            scores = results[metric][k]
            final_results[metric][k] = sum(scores) / len(scores) if scores else 0.0
    
    final_results['map'] = results['map']
    
    return final_results


def collaborative_filtering_for_evaluation(user_id, cursor, excluded_applications: Set[int] = None):
    """
    Collaborative filtering for evaluation with train/test split support.
    This version allows excluding certain applications (test set) from the user's history.
    
    Args:
        user_id: User ID
        cursor: Database cursor
        excluded_applications: Set of internship IDs to exclude from user's application history
                              (these are the test items we want to predict)
    
    Returns:
        List of recommendation dictionaries
    """
    if excluded_applications is None:
        excluded_applications = set()
    
    # Get all applications
    cursor.execute("SELECT student_id, internship_id FROM applications")
    all_applications = cursor.fetchall()
    
    # Build user-item matrix
    user_items = {}
    for app in all_applications:
        student_id = app['student_id']
        internship_id = app['internship_id']
        if student_id not in user_items:
            user_items[student_id] = set()
        user_items[student_id].add(internship_id)
    
    # For the target user, exclude test set applications from their history
    # This simulates a train/test split
    current_user_apps = user_items.get(user_id, set()) - excluded_applications
    
    # If user has no applications left after excluding test set, skip
    if not current_user_apps:
        return []
    
    # Find similar students based on Jaccard similarity (using training set only)
    similar_students = []
    
    for student_id, apps in user_items.items():
        if student_id == user_id:
            continue
            
        intersection = len(current_user_apps & apps)
        union = len(current_user_apps | apps)
        similarity = intersection / union if union > 0 else 0
        
        if similarity > 0:
            similar_students.append((student_id, similarity))
    
    # Sort by similarity
    similar_students.sort(key=lambda x: x[1], reverse=True)
    
    # Get top internships from similar students
    recommendations = []
    seen_internships = set(current_user_apps)  # Exclude internships in training set
    
    for student_id, similarity in similar_students[:3]:  # Top 3 similar students
        for internship_id in user_items[student_id]:
            if internship_id not in seen_internships:
                cursor.execute("SELECT * FROM internships WHERE id=?", (internship_id,))
                internship = cursor.fetchone()
                if internship:
                    # Get company information
                    cursor.execute("SELECT name FROM users WHERE id=?", (internship['company_id'],))
                    company = cursor.fetchone()
                    company_name = company['name'] if company else 'Unknown Company'
                    
                    recommendations.append({
                        'id': internship['id'],
                        'title': internship['title'],
                        'description': internship['description'],
                        'required_skills': internship['required_skills'],
                        'posted_at': internship['posted_at'],
                        'company_name': company_name,
                        'company_id': internship['company_id'],
                        'similarity': similarity,
                        'type': 'Collaborative'
                    })
                    seen_internships.add(internship_id)
    
    return recommendations[:20]  # Return more recommendations for evaluation


def evaluate_collaborative_filtering(
    conn: sqlite3.Connection,
    user_ids: List[int],
    ground_truth: Dict[int, List[int]],
    k_values: List[int] = [5, 10, 20],
    test_split_ratio: float = 0.2
) -> Dict[str, Dict[int, float]]:
    """
    Evaluate Collaborative Filtering algorithm using train/test split.
    
    For collaborative filtering, we use a train/test split approach:
    - Training set: Part of user's applications (used to find similar students)
    - Test set: Remaining applications (what we try to predict)
    - Recommendations are compared against the test set
    
    Args:
        conn: Database connection
        user_ids: List of user IDs to evaluate
        ground_truth: Dictionary mapping user_id to list of applied internship IDs
        k_values: List of K values for evaluation
        test_split_ratio: Ratio of applications to use as test set (default 0.2 = 20%)
    
    Returns:
        Dictionary with metrics: {'precision': {k: score}, 'recall': {k: score}, ...}
    """
    import random
    random.seed(42)  # For reproducibility
    
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    
    results = {
        'precision': defaultdict(list),
        'recall': defaultdict(list),
        'ndcg': defaultdict(list),
        'map': {}
    }
    
    recommendations = {}
    test_ground_truth = {}
    
    for user_id in user_ids:
        if user_id not in ground_truth:
            continue
        
        user_applications = ground_truth[user_id]
        
        # Skip users with too few applications (need at least 2 for train/test split)
        if len(user_applications) < 2:
            continue
        
        # Split applications into train and test sets
        shuffled_apps = user_applications.copy()
        random.shuffle(shuffled_apps)
        
        test_size = max(1, int(len(shuffled_apps) * test_split_ratio))
        test_set = set(shuffled_apps[:test_size])
        train_set = set(shuffled_apps[test_size:])
        
        # Get collaborative filtering recommendations using training set only
        try:
            recs = collaborative_filtering_for_evaluation(user_id, cursor, excluded_applications=test_set)
            recommended_ids = [rec['id'] for rec in recs]
            recommendations[user_id] = recommended_ids
            
            # Use test set as ground truth (what we're trying to predict)
            test_ground_truth[user_id] = list(test_set)
            relevant_ids = list(test_set)
            
            # Calculate metrics for each k
            for k in k_values:
                precision = calculate_precision_at_k(recommended_ids, relevant_ids, k)
                recall = calculate_recall_at_k(recommended_ids, relevant_ids, k)
                ndcg = calculate_ndcg(recommended_ids, relevant_ids, k)
                
                results['precision'][k].append(precision)
                results['recall'][k].append(recall)
                results['ndcg'][k].append(ndcg)
        except Exception as e:
            print(f"Error evaluating collaborative for user {user_id}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Calculate MAP using test set as ground truth
    results['map'] = calculate_map(recommendations, test_ground_truth, k_values)
    
    # Average metrics across users
    final_results = {}
    for metric in ['precision', 'recall', 'ndcg']:
        final_results[metric] = {}
        for k in k_values:
            scores = results[metric][k]
            final_results[metric][k] = sum(scores) / len(scores) if scores else 0.0
    
    final_results['map'] = results['map']
    
    return final_results


def evaluate_hybrid(
    conn: sqlite3.Connection,
    user_ids: List[int],
    ground_truth: Dict[int, List[int]],
    k_values: List[int] = [5, 10, 20]
) -> Dict[str, Dict[int, float]]:
    """
    Evaluate Hybrid (Content-Based + Collaborative) algorithm.
    
    Returns:
        Dictionary with metrics: {'precision': {k: score}, 'recall': {k: score}, ...}
    """
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    
    results = {
        'precision': defaultdict(list),
        'recall': defaultdict(list),
        'ndcg': defaultdict(list),
        'map': {}
    }
    
    recommendations = {}
    
    for user_id in user_ids:
        if user_id not in ground_truth:
            continue
        
        # Get hybrid recommendations by manually combining content and collaborative
        try:
            # Get content-based recommendations
            content_recs = content_based_recommendations(user_id, cursor)
            
            # Get collaborative filtering recommendations
            collab_recs = collaborative_filtering(user_id, cursor)
            
            # Combine and deduplicate (same logic as get_recommendations)
            all_recs = {rec['id']: rec for rec in content_recs}
            
            # Add collaborative recommendations (keep higher similarity if duplicate)
            for rec in collab_recs:
                if rec['id'] not in all_recs:
                    all_recs[rec['id']] = rec
                else:
                    # If collaborative recommendation has higher similarity, use it
                    if rec['similarity'] > all_recs[rec['id']]['similarity']:
                        all_recs[rec['id']] = rec
            
            recommended_ids = [rec['id'] for rec in list(all_recs.values())]
            recommendations[user_id] = recommended_ids
            
            relevant_ids = ground_truth[user_id]
            
            # Calculate metrics for each k
            for k in k_values:
                precision = calculate_precision_at_k(recommended_ids, relevant_ids, k)
                recall = calculate_recall_at_k(recommended_ids, relevant_ids, k)
                ndcg = calculate_ndcg(recommended_ids, relevant_ids, k)
                
                results['precision'][k].append(precision)
                results['recall'][k].append(recall)
                results['ndcg'][k].append(ndcg)
        except Exception as e:
            print(f"Error evaluating hybrid for user {user_id}: {e}")
            continue
    
    # Calculate MAP
    results['map'] = calculate_map(recommendations, ground_truth, k_values)
    
    # Average metrics across users
    final_results = {}
    for metric in ['precision', 'recall', 'ndcg']:
        final_results[metric] = {}
        for k in k_values:
            scores = results[metric][k]
            final_results[metric][k] = sum(scores) / len(scores) if scores else 0.0
    
    final_results['map'] = results['map']
    
    return final_results


# ============================================================================
# A/B TESTING FRAMEWORK
# ============================================================================

class ABTest:
    """
    A/B Testing framework for comparing recommendation algorithms.
    """
    
    def __init__(self, conn: sqlite3.Connection, group_a_algorithm: str, group_b_algorithm: str):
        """
        Initialize A/B test.
        
        Args:
            conn: Database connection
            group_a_algorithm: Algorithm name for group A ('content', 'collaborative', 'hybrid')
            group_b_algorithm: Algorithm name for group B
        """
        self.conn = conn
        self.group_a_algorithm = group_a_algorithm
        self.group_b_algorithm = group_b_algorithm
        self.group_a_users = []
        self.group_b_users = []
        
    def split_users(self, user_ids: List[int], split_ratio: float = 0.5, random_seed: Optional[int] = None):
        """
        Split users into two groups for A/B testing.
        
        Args:
            user_ids: List of user IDs to split
            split_ratio: Ratio for group A (default 0.5 = 50/50 split)
            random_seed: Optional random seed for reproducibility
        """
        import random
        if random_seed is not None:
            random.seed(random_seed)
        
        shuffled = user_ids.copy()
        random.shuffle(shuffled)
        
        split_point = int(len(shuffled) * split_ratio)
        self.group_a_users = shuffled[:split_point]
        self.group_b_users = shuffled[split_point:]
        
        print(f"A/B Test Split:")
        print(f"  Group A ({self.group_a_algorithm}): {len(self.group_a_users)} users")
        print(f"  Group B ({self.group_b_algorithm}): {len(self.group_b_users)} users")
    
    def run_ab_test(self, k_values: List[int] = [5, 10, 20]) -> Dict[str, Dict]:
        """
        Run A/B test and compare algorithms.
        
        Returns:
            Dictionary with results for both groups
        """
        ground_truth = get_ground_truth(self.conn)
        
        # Evaluate Group A
        print(f"\nEvaluating Group A: {self.group_a_algorithm}")
        group_a_results = self._evaluate_algorithm(
            self.group_a_algorithm,
            self.group_a_users,
            ground_truth,
            k_values
        )
        
        # Evaluate Group B
        print(f"\nEvaluating Group B: {self.group_b_algorithm}")
        group_b_results = self._evaluate_algorithm(
            self.group_b_algorithm,
            self.group_b_users,
            ground_truth,
            k_values
        )
        
        return {
            'group_a': {
                'algorithm': self.group_a_algorithm,
                'users': len(self.group_a_users),
                'results': group_a_results
            },
            'group_b': {
                'algorithm': self.group_b_algorithm,
                'users': len(self.group_b_users),
                'results': group_b_results
            }
        }
    
    def _evaluate_algorithm(self, algorithm: str, user_ids: List[int], 
                           ground_truth: Dict[int, List[int]], k_values: List[int]) -> Dict:
        """Evaluate a specific algorithm."""
        if algorithm == 'content':
            return evaluate_content_based(self.conn, user_ids, ground_truth, k_values)
        elif algorithm == 'collaborative':
            return evaluate_collaborative_filtering(self.conn, user_ids, ground_truth, k_values)
        elif algorithm == 'hybrid':
            return evaluate_hybrid(self.conn, user_ids, ground_truth, k_values)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


# ============================================================================
# COMPREHENSIVE EVALUATION REPORT
# ============================================================================

def generate_evaluation_report(
    content_results: Dict,
    collaborative_results: Dict,
    hybrid_results: Dict,
    output_file: str = "evaluation_report.json"
) -> Dict:
    """
    Generate comprehensive evaluation report comparing all three algorithms.
    
    Args:
        content_results: Results from content-based evaluation
        collaborative_results: Results from collaborative filtering evaluation
        hybrid_results: Results from hybrid evaluation
        output_file: Path to save JSON report
    
    Returns:
        Comprehensive evaluation report dictionary
    """
    report = {
        'timestamp': datetime.now().isoformat(),
        'algorithms': {
            'content_based': content_results,
            'collaborative_filtering': collaborative_results,
            'hybrid': hybrid_results
        },
        'comparison': {},
        'summary': {}
    }
    
    # Compare algorithms
    k_values = list(content_results.get('precision', {}).keys())
    
    comparison = {}
    for metric in ['precision', 'recall', 'ndcg', 'map']:
        comparison[metric] = {}
        for k in k_values:
            content_score = content_results.get(metric, {}).get(k, 0.0)
            collab_score = collaborative_results.get(metric, {}).get(k, 0.0)
            hybrid_score = hybrid_results.get(metric, {}).get(k, 0.0)
            
            comparison[metric][k] = {
                'content_based': content_score,
                'collaborative_filtering': collab_score,
                'hybrid': hybrid_score,
                'best_algorithm': max(
                    [('content_based', content_score),
                     ('collaborative_filtering', collab_score),
                     ('hybrid', hybrid_score)],
                    key=lambda x: x[1]
                )[0]
            }
    
    report['comparison'] = comparison
    
    # Generate summary
    summary = {
        'best_overall': {},
        'recommendations': []
    }
    
    for metric in ['precision', 'recall', 'ndcg', 'map']:
        best_scores = {}
        for k in k_values:
            scores = comparison[metric][k]
            best_algo = scores['best_algorithm']
            best_score = scores[best_algo]
            best_scores[k] = {
                'algorithm': best_algo,
                'score': best_score
            }
        summary['best_overall'][metric] = best_scores
    
    # Generate recommendations
    recommendations = []
    for metric in ['precision', 'recall', 'ndcg']:
        for k in k_values:
            scores = comparison[metric][k]
            if scores['hybrid'] >= scores['content_based'] and scores['hybrid'] >= scores['collaborative_filtering']:
                recommendations.append(f"Hybrid performs best for {metric.upper()}@{k}")
            elif scores['content_based'] >= scores['collaborative_filtering']:
                recommendations.append(f"Content-Based performs best for {metric.upper()}@{k}")
            else:
                recommendations.append(f"Collaborative performs best for {metric.upper()}@{k}")
    
    summary['recommendations'] = recommendations
    report['summary'] = summary
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nEvaluation report saved to: {output_file}")
    
    return report


def print_evaluation_report(report: Dict):
    """
    Print formatted evaluation report to console.
    """
    print("\n" + "="*80)
    print("COMPREHENSIVE EVALUATION REPORT")
    print("="*80)
    print(f"Generated at: {report['timestamp']}\n")
    
    algorithms = report['algorithms']
    comparison = report['comparison']
    
    # Print metrics comparison
    for metric in ['precision', 'recall', 'ndcg', 'map']:
        print(f"\n{metric.upper().replace('_', ' ')}:")
        print("-" * 80)
        print(f"{'K':<10} {'Content-Based':<20} {'Collaborative':<20} {'Hybrid':<20} {'Best':<15}")
        print("-" * 80)
        
        for k in sorted(comparison[metric].keys()):
            scores = comparison[metric][k]
            content = scores['content_based']
            collab = scores['collaborative_filtering']
            hybrid = scores['hybrid']
            best = scores['best_algorithm']
            
            print(f"{k:<10} {content:<20.4f} {collab:<20.4f} {hybrid:<20.4f} {best:<15}")
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY & RECOMMENDATIONS")
    print("="*80)
    for rec in report['summary']['recommendations'][:10]:  # Show first 10
        print(f"  • {rec}")


# ============================================================================
# MAIN EVALUATION FUNCTION
# ============================================================================

def run_comprehensive_evaluation(
    db_path: str = "internship.db",
    k_values: List[int] = [5, 10, 20],
    output_file: str = "evaluation_report.json",
    ab_test: bool = False
) -> Dict:
    """
    Run comprehensive offline evaluation for all three algorithms.
    
    Args:
        db_path: Path to database file
        k_values: List of K values to evaluate
        output_file: Path to save evaluation report
        ab_test: Whether to run A/B testing
    
    Returns:
        Comprehensive evaluation report
    """
    # Connect to database
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return {}
    
    # For evaluation, we need to mock Flask app context
    # Create a direct SQLite connection instead
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    print("="*80)
    print("OFFLINE EVALUATION - INTERNSHIP RECOMMENDATION SYSTEM")
    print("="*80)
    print(f"Database: {db_path}")
    print(f"K values: {k_values}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    # Get ground truth and user IDs
    print("Loading ground truth data...")
    ground_truth = get_ground_truth(conn)
    user_ids = list(ground_truth.keys())
    
    print(f"Found {len(user_ids)} users with application history")
    print(f"Total applications: {sum(len(apps) for apps in ground_truth.values())}\n")
    
    if not user_ids:
        print("Warning: No users with application history found. Evaluation requires ground truth data.")
        conn.close()
        return {}
    
    # Evaluate Content-Based Filtering
    print("Evaluating Content-Based Filtering...")
    content_results = evaluate_content_based(conn, user_ids, ground_truth, k_values)
    
    # Evaluate Collaborative Filtering
    print("Evaluating Collaborative Filtering...")
    collaborative_results = evaluate_collaborative_filtering(conn, user_ids, ground_truth, k_values)
    
    # Evaluate Hybrid Approach
    print("Evaluating Hybrid Approach...")
    hybrid_results = evaluate_hybrid(conn, user_ids, ground_truth, k_values)
    
    # Generate comprehensive report
    print("\nGenerating evaluation report...")
    report = generate_evaluation_report(
        content_results,
        collaborative_results,
        hybrid_results,
        output_file
    )
    
    # Print report
    print_evaluation_report(report)
    
    # Run A/B testing if requested
    if ab_test:
        print("\n" + "="*80)
        print("A/B TESTING")
        print("="*80)
        
        ab_test_instance = ABTest(conn, 'content', 'hybrid')
        ab_test_instance.split_users(user_ids, split_ratio=0.5, random_seed=42)
        ab_results = ab_test_instance.run_ab_test(k_values)
        
        print("\nA/B Test Results:")
        print(json.dumps(ab_results, indent=2))
        
        report['ab_test'] = ab_results
    
    conn.close()
    
    return report


# ============================================================================
# USER SURVEY & FEEDBACK (Online Evaluation Support)
# ============================================================================

def collect_user_feedback(user_id: int, internship_id: int, rating: int, feedback: str = "") -> Dict:
    """
    Collect user feedback for online evaluation.
    
    Args:
        user_id: User ID
        internship_id: Internship ID
        rating: Rating (1-5 scale)
        feedback: Optional feedback text
    
    Returns:
        Feedback record dictionary
    """
    feedback_record = {
        'user_id': user_id,
        'internship_id': internship_id,
        'rating': rating,
        'feedback': feedback,
        'timestamp': datetime.now().isoformat()
    }
    
    # In a real system, this would save to database
    # For now, return the record
    return feedback_record


def analyze_user_surveys(feedback_data: List[Dict]) -> Dict:
    """
    Analyze user survey feedback.
    
    Args:
        feedback_data: List of feedback records
    
    Returns:
        Analysis results
    """
    if not feedback_data:
        return {}
    
    total_feedback = len(feedback_data)
    avg_rating = sum(f['rating'] for f in feedback_data) / total_feedback
    
    rating_distribution = defaultdict(int)
    for f in feedback_data:
        rating_distribution[f['rating']] += 1
    
    return {
        'total_feedback': total_feedback,
        'average_rating': avg_rating,
        'rating_distribution': dict(rating_distribution),
        'satisfaction_rate': sum(1 for f in feedback_data if f['rating'] >= 4) / total_feedback
    }


# ============================================================================
# ALGORITHM-SPECIFIC VALIDATION
# ============================================================================

def validate_content_based_algorithm(conn: sqlite3.Connection) -> Dict:
    """
    Validate Content-Based algorithm specific characteristics.
    """
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    
    # Check if users have skills
    cursor.execute("SELECT COUNT(*) as count FROM profiles WHERE skills IS NOT NULL AND skills != ''")
    users_with_skills = cursor.fetchone()['count']
    
    # Check if internships have required skills
    cursor.execute("SELECT COUNT(*) as count FROM internships WHERE required_skills IS NOT NULL AND required_skills != ''")
    internships_with_skills = cursor.fetchone()['count']
    
    return {
        'users_with_skills': users_with_skills,
        'internships_with_skills': internships_with_skills,
        'coverage': users_with_skills > 0 and internships_with_skills > 0
    }


def validate_collaborative_filtering_algorithm(conn: sqlite3.Connection) -> Dict:
    """
    Validate Collaborative Filtering algorithm specific characteristics.
    """
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    
    # Check application sparsity
    cursor.execute("SELECT COUNT(DISTINCT student_id) as users, COUNT(DISTINCT internship_id) as internships, COUNT(*) as applications FROM applications")
    stats = cursor.fetchone()
    
    users = stats['users']
    internships = stats['internships']
    applications = stats['applications']
    
    # Calculate sparsity
    total_possible = users * internships if users > 0 and internships > 0 else 1
    sparsity = 1 - (applications / total_possible) if total_possible > 0 else 1.0
    
    # Check cold start problem (users with no applications)
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'student'")
    total_students = cursor.fetchone()['count']
    
    users_with_apps = users
    cold_start_users = total_students - users_with_apps
    
    return {
        'total_students': total_students,
        'users_with_applications': users_with_apps,
        'cold_start_users': cold_start_users,
        'sparsity': sparsity,
        'average_applications_per_user': applications / users if users > 0 else 0
    }


def validate_hybrid_algorithm(conn: sqlite3.Connection) -> Dict:
    """
    Validate Hybrid algorithm characteristics.
    """
    content_validation = validate_content_based_algorithm(conn)
    collaborative_validation = validate_collaborative_filtering_algorithm(conn)
    
    return {
        'content_based': content_validation,
        'collaborative_filtering': collaborative_validation,
        'hybrid_ready': content_validation['coverage'] and collaborative_validation['users_with_applications'] > 0
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Offline Evaluation for Internship Recommendation System')
    parser.add_argument('--db', type=str, default='internship.db', help='Path to database file')
    parser.add_argument('--k', type=int, nargs='+', default=[5, 10, 20], help='K values for evaluation')
    parser.add_argument('--output', type=str, default='evaluation_report.json', help='Output file for report')
    parser.add_argument('--ab-test', action='store_true', help='Run A/B testing')
    parser.add_argument('--validate', action='store_true', help='Run algorithm-specific validation')
    
    args = parser.parse_args()
    
    # Run validation if requested
    if args.validate:
        print("="*80)
        print("ALGORITHM-SPECIFIC VALIDATION")
        print("="*80)
        
        conn = sqlite3.connect(args.db)
        conn.row_factory = sqlite3.Row
        
        print("\nContent-Based Algorithm Validation:")
        content_val = validate_content_based_algorithm(conn)
        print(json.dumps(content_val, indent=2))
        
        print("\nCollaborative Filtering Algorithm Validation:")
        collab_val = validate_collaborative_filtering_algorithm(conn)
        print(json.dumps(collab_val, indent=2))
        
        print("\nHybrid Algorithm Validation:")
        hybrid_val = validate_hybrid_algorithm(conn)
        print(json.dumps(hybrid_val, indent=2))
        
        conn.close()
        print("\n")
    
    # Run comprehensive evaluation
    report = run_comprehensive_evaluation(
        db_path=args.db,
        k_values=args.k,
        output_file=args.output,
        ab_test=args.ab_test
    )
    
    print("\n" + "="*80)
    print("EVALUATION COMPLETE")
    print("="*80)

