# Algorithms Used in Internship Recommendation System

## Overview
This project uses a **Hybrid Recommendation System** that combines three different algorithms to provide personalized internship recommendations to students.

---

## 🎯 Main Algorithms

### 1. **Content-Based Filtering** (Skill Matching)
### 2. **CV-Based Recommendations** (Enhanced Content Filtering)
### 3. **Collaborative Filtering** (User-Based)

---

## 1️⃣ Content-Based Filtering Algorithm

### **Purpose**
Recommends internships based on matching student skills with required skills.

### **How It Works**

#### Step 1: Get Student Skills
```python
# Extract skills from student profile
student_skills = set(skill.strip().lower() for skill in profile['skills'].split(','))
# Example: {'python', 'javascript', 'react', 'sql'}
```

#### Step 2: Get All Internships
```python
# Fetch all available internships from database
internships = cursor.fetchall()
```

#### Step 3: Calculate Similarity Using **Jaccard Similarity**

**Formula:**
```
Jaccard Similarity = |A ∩ B| / |A ∪ B|

Where:
A = Student skills
B = Required skills for internship
∩ = Intersection (common skills)
∪ = Union (all unique skills)
```

**Example:**
```python
Student Skills:     {'python', 'javascript', 'react', 'sql'}
Required Skills:    {'python', 'react', 'html', 'css'}

Intersection:       {'python', 'react'}  → 2 skills
Union:             {'python', 'javascript', 'react', 'sql', 'html', 'css'}  → 6 skills

Similarity = 2/6 = 0.33 (33% match)
```

#### Step 4: Filter and Rank
```python
# Only recommend if similarity > 0.2 (20% threshold)
if similarity > 0.2:
    recommendations.append(internship)

# Sort by similarity (highest first)
recommendations.sort(key=lambda x: x['similarity'], reverse=True)

# Return top 5
return recommendations[:5]
```

### **Advantages**
- ✅ Personalized to each student
- ✅ Based on actual skills
- ✅ Easy to understand and explain
- ✅ No cold start problem (works for new students)

### **Limitations**
- ❌ Limited to exact skill matching
- ❌ Doesn't consider student experience or education

---

## 2️⃣ CV-Based Recommendations Algorithm

### **Purpose**
Enhanced content filtering using comprehensive CV data including skills, experience, and education.

### **How It Works**

#### Step 1: Extract Information from CV
```python
# Extract skills from multiple CV sections:
- Certifications field (contains skills)
- Work Experience
- Projects
- Education
```

#### Step 2: Text Mining for Skills
```python
# Search for technical skills in CV text
tech_skills = ['python', 'java', 'javascript', 'react', 'node', 'sql', ...]

for skill in tech_skills:
    if skill in cv_text.lower():
        cv_skills.add(skill)
```

#### Step 3: Multi-Factor Similarity Score

**Components:**

**a) Skill Similarity** (Jaccard)
```
skill_similarity = |CV_skills ∩ Required_skills| / |CV_skills ∪ Required_skills|
```

**b) Education Bonus** (+0.1 if degree mentioned)
```python
if 'bachelor' or 'master' or 'phd' in cv['education']:
    education_bonus = 0.1
```

**c) Experience Bonus** (+0.1 if relevant experience)
```python
if 'intern' or 'developer' or 'programmer' in cv['work_experience']:
    experience_bonus = 0.1
```

**d) Total Similarity**
```
total_similarity = skill_similarity + education_bonus + experience_bonus
```

#### Step 4: Filter and Rank
```python
# Lower threshold (0.15) to capture more matches
if total_similarity > 0.15:
    recommendations.append(internship)

# Sort by total similarity
recommendations.sort(key=lambda x: x['similarity'], reverse=True)
return recommendations[:5]
```

### **Example Calculation**

```
CV Skills:          {'python', 'flask', 'sql'}
Required Skills:    {'python', 'django', 'sql'}

Skill Match:        2/4 = 0.50
Education:          Has Bachelor's = +0.10
Experience:         Has internship exp = +0.10

Total Similarity:   0.50 + 0.10 + 0.10 = 0.70 (70% match!)
```

### **Advantages**
- ✅ More comprehensive than skill-only matching
- ✅ Considers education level
- ✅ Factors in work experience
- ✅ Better quality recommendations

### **Limitations**
- ❌ Requires complete CV
- ❌ Text mining limited to predefined skill list
- ❌ Simple keyword matching (not NLP)

---

## 3️⃣ Collaborative Filtering Algorithm

### **Purpose**
Recommends internships based on what similar students applied to ("Students like you also applied to...")

### **How It Works**

#### Step 1: Build User-Item Matrix
```python
user_items = {
    student1: {internship1, internship2, internship3},
    student2: {internship1, internship4},
    student3: {internship2, internship3, internship5},
    ...
}
```

#### Step 2: Find Similar Students Using **Jaccard Similarity**

**Formula:**
```
Similarity(User A, User B) = |Applications_A ∩ Applications_B| / |Applications_A ∪ Applications_B|
```

**Example:**
```python
Current Student Applied:  {internship1, internship2, internship3}
Other Student Applied:    {internship2, internship3, internship4, internship5}

Intersection:             {internship2, internship3}  → 2 common
Union:                   {1, 2, 3, 4, 5}  → 5 total

Similarity = 2/5 = 0.40 (40% similar)
```

#### Step 3: Get Recommendations from Similar Students
```python
# Get top 3 most similar students
similar_students = sorted(students, key=similarity, reverse=True)[:3]

# Recommend internships they applied to that current student hasn't
for similar_student in similar_students:
    for internship in similar_student.applications:
        if internship not in current_student.applications:
            recommendations.append(internship)
```

#### Step 4: Filter Already Applied
```python
# Don't recommend internships student already applied to
seen_internships = set(current_user_apps)
```

### **Example Scenario**

```
You (Student A):
Applied to: [Python Internship, Web Dev Internship]

Similar Student (Student B) - 60% similar:
Applied to: [Python Internship, Web Dev Internship, ML Internship, Data Science Internship]

Recommendations for You:
→ ML Internship (because similar student applied)
→ Data Science Internship (because similar student applied)
```

### **Advantages**
- ✅ Discovers unexpected good matches
- ✅ Leverages wisdom of the crowd
- ✅ Works even if skill data is incomplete

### **Limitations**
- ❌ Cold start problem (needs application history)
- ❌ Sparsity problem (few applications = poor recommendations)
- ❌ Popular bias (recommends popular internships)

---

## 🔄 Hybrid Combination Strategy

### **How All Three Are Combined**

```python
def get_recommendations(user_id):
    # Get recommendations from all three algorithms
    content_recs = content_based_recommendations(user_id)
    cv_recs = cv_based_recommendations(user_id)
    collab_recs = collaborative_filtering(user_id)
    
    # Combine and deduplicate
    all_recs = {}
    
    # Add content-based
    for rec in content_recs:
        all_recs[rec['id']] = rec
    
    # Add CV-based (override if higher similarity)
    for rec in cv_recs:
        if rec['id'] not in all_recs:
            all_recs[rec['id']] = rec
        elif rec['similarity'] > all_recs[rec['id']]['similarity']:
            all_recs[rec['id']] = rec  # Use higher score
    
    # Add collaborative
    for rec in collab_recs:
        if rec['id'] not in all_recs:
            all_recs[rec['id']] = rec
    
    return list(all_recs.values())
```

### **Deduplication Strategy**
1. Start with content-based recommendations
2. Add CV-based, but if same internship exists, use **higher similarity score**
3. Add collaborative, but only if not already recommended

### **Result**
- **Diverse recommendations** from multiple perspectives
- **Best scores** kept (if same internship recommended by multiple algorithms)
- **No duplicates** in final list

---

## 📊 Comparison Table

| Feature | Content-Based | CV-Based | Collaborative |
|---------|--------------|----------|---------------|
| **Input** | Profile skills | Full CV | Application history |
| **Algorithm** | Jaccard similarity | Multi-factor scoring | User-based CF |
| **Complexity** | Low | Medium | Medium |
| **Cold Start** | ✅ Works | ✅ Works | ❌ Needs data |
| **Accuracy** | Medium | High | Variable |
| **Diversity** | Low | Medium | High |
| **Explainability** | ✅ Clear | ✅ Clear | ⚠️ Less clear |

---

## 🎯 Key Metrics & Thresholds

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **Content-based threshold** | 0.2 (20%) | Minimum similarity to recommend |
| **CV-based threshold** | 0.15 (15%) | Lower for more matches |
| **Education bonus** | +0.1 | Boost for degree holders |
| **Experience bonus** | +0.1 | Boost for relevant experience |
| **Top similar students** | 3 | Number of users for collaborative |
| **Max recommendations** | 5 per algorithm | Prevents overwhelming user |

---

## 🔬 Mathematical Formulas Used

### 1. Jaccard Similarity Index
```
J(A, B) = |A ∩ B| / |A ∪ B| = |A ∩ B| / (|A| + |B| - |A ∩ B|)

Range: [0, 1]
0 = No similarity
1 = Identical sets
```

### 2. CV-Based Scoring
```
Score = Jaccard(CV_skills, Required_skills) + Education_bonus + Experience_bonus

Where:
- Jaccard ∈ [0, 1]
- Education_bonus ∈ {0, 0.1}
- Experience_bonus ∈ {0, 0.1}

Maximum possible score: 1.2
```

### 3. User Similarity (Collaborative)
```
Sim(u, v) = |Apps_u ∩ Apps_v| / |Apps_u ∪ Apps_v|

Where:
Apps_u = Internships applied by user u
Apps_v = Internships applied by user v
```

---

## 💡 Why This Hybrid Approach?

### **Strengths**
1. **Redundancy**: If one algorithm fails, others still work
2. **Diversity**: Different perspectives on what's relevant
3. **Accuracy**: CV-based provides most accurate matches
4. **Discovery**: Collaborative finds unexpected good fits
5. **Robustness**: Works for both new and experienced users

### **Use Cases**
- **New students**: Content + CV-based work well
- **Active students**: All three algorithms contribute
- **Students without CV**: Content + Collaborative still work

---

## 🚀 Future Enhancements

### Possible Improvements:
1. **TF-IDF** for better text analysis
2. **Cosine Similarity** as alternative to Jaccard
3. **Matrix Factorization** for collaborative filtering
4. **Deep Learning** for skill extraction from CV
5. **Feedback Loop** to improve over time
6. **A/B Testing** to measure effectiveness

---

## 📝 Summary

**Main Algorithm**: **Hybrid Recommendation System**

**Components**:
1. ✅ Content-Based (Jaccard Similarity)
2. ✅ CV-Based (Multi-factor scoring)
3. ✅ Collaborative Filtering (User-based)

**Similarity Metric**: **Jaccard Index** (for all three)

**Combination**: **Score-based deduplication** with highest similarity preference

**Result**: **Personalized, accurate, and diverse internship recommendations** 🎯

