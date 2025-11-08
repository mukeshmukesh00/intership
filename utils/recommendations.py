# utils/recommendations.py - Recommendation algorithms
from .database import get_db

def get_recommendations(user_id):
    """Get personalized internship recommendations for a user."""
    conn = get_db()
    irs = conn.cursor()
    
    # Content-based recommendations
    content_recs = content_based_recommendations(user_id, irs)
    
    # Collaborative filtering recommendations
    collab_recs = collaborative_filtering(user_id, irs)
    
    # Combine and deduplicate recommendations
    all_recs = {rec['id']: rec for rec in content_recs}
    
    # Add collaborative recommendations (keep higher similarity if duplicate)
    for rec in collab_recs:
        if rec['id'] not in all_recs:
            all_recs[rec['id']] = rec
        else:
            # If collaborative recommendation has higher similarity, use it
            if rec['similarity'] > all_recs[rec['id']]['similarity']:
                all_recs[rec['id']] = rec
    
    return list(all_recs.values())

def content_based_recommendations(user_id, irs):
    """Content-based recommendation algorithm using skill matching."""
    # Get student's skills
    irs.execute("SELECT skills FROM profiles WHERE user_id=?", (user_id,))
    profile = irs.fetchone()
    
    if not profile or not profile['skills']:
        return []
    
    student_skills = set(skill.strip().lower() for skill in profile['skills'].split(','))
    
    # Get all internships
    irs.execute("SELECT * FROM internships")
    internships = irs.fetchall()
    
    # Calculate similarity for each internship
    recommendations = []
    for internship in internships:
        required_skills = set(skill.strip().lower() for skill in internship['required_skills'].split(',')) if internship['required_skills'] else set()
        
        if not required_skills:
            continue
            
        # Jaccard similarity
        intersection = len(student_skills & required_skills)
        union = len(student_skills | required_skills)
        similarity = intersection / union if union > 0 else 0
        
        if similarity > 0.2:  # Threshold
            # Get company information
            irs.execute("SELECT name FROM users WHERE id=?", (internship['company_id'],))
            company = irs.fetchone()
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
                'type': 'Content-based'
            })
    
    # Sort by similarity
    recommendations.sort(key=lambda x: x['similarity'], reverse=True)
    return recommendations[:5]

def collaborative_filtering(user_id, irs):
    """Collaborative filtering recommendation algorithm."""
    # Get applications of similar students
    # Step 1: Find students with similar applications
    irs.execute("SELECT student_id, internship_id FROM applications")
    all_applications = irs.fetchall()
    
    # Build user-item matrix
    user_items = {}
    for app in all_applications:
        student_id = app['student_id']
        internship_id = app['internship_id']
        if student_id not in user_items:
            user_items[student_id] = set()
        user_items[student_id].add(internship_id)
    
    # Find similar students based on Jaccard similarity
    current_user_apps = user_items.get(user_id, set())
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
    seen_internships = set(current_user_apps)  # Exclude internships already applied to
    
    for student_id, similarity in similar_students[:3]:  # Top 3 similar students
        for internship_id in user_items[student_id]:
            if internship_id not in seen_internships:
                irs.execute("SELECT * FROM internships WHERE id=?", (internship_id,))
                internship = irs.fetchone()
                if internship:
                    # Get company information
                    irs.execute("SELECT name FROM users WHERE id=?", (internship['company_id'],))
                    company = irs.fetchone()
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
    
    return recommendations[:5]  # Top 5
