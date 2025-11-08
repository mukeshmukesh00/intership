# How to View the Database and Data

## 📊 **Your Database File**

**Location:** `D:\Final-Project-main\internship.db`  
**Type:** SQLite3 Database  
**Tables:** 6 tables (users, profiles, internships, applications, messages, cvs)

---

## 🔍 **Method 1: Using Python Script (EASIEST)**

I've created a simple script for you!

### **Step 1: Run the script**
```bash
python view_database.py
```

### **What it shows:**
- ✅ All tables in the database
- ✅ Column names for each table
- ✅ Number of rows in each table
- ✅ First 10 rows of data from each table
- ✅ Formatted, easy-to-read output

### **Output Example:**
```
================================================================================
INTERNSHIP DATABASE VIEWER
================================================================================

📊 Total Tables: 6
Tables: applications, cvs, internships, messages, profiles, users

================================================================================
TABLE: USERS
================================================================================
Columns: id, email, password, role, name, created_at

Total Rows: 5

Data (showing first 5 rows):

Row 1:
  id: 1
  email: student1@example.com
  password: pbkdf2:sha256:260000$...
  role: student
  name: John Doe
  created_at: 2025-10-30 12:34:56
...
```

---

## 🖥️ **Method 2: Using DB Browser for SQLite (GUI - BEST FOR BEGINNERS)**

This is a free, visual tool - very user-friendly!

### **Step 1: Download**
1. Go to: https://sqlitebrowser.org/
2. Download for Windows
3. Install (it's free!)

### **Step 2: Open Database**
1. Open DB Browser for SQLite
2. Click **"Open Database"**
3. Navigate to: `D:\Final-Project-main\`
4. Select `internship.db`
5. Click **Open**

### **Step 3: View Data**
- **Browse Data** tab → Select table → See all data
- **Database Structure** tab → See table schemas
- **Execute SQL** tab → Run custom queries

### **Features:**
- ✅ Visual table browser
- ✅ Edit data directly
- ✅ Run SQL queries
- ✅ Export data (CSV, SQL)
- ✅ Search and filter
- ✅ Very beginner-friendly!

**Screenshot of what you'll see:**
```
┌─────────────────────────────────────┐
│  Users Table                        │
├────┬──────────────┬──────┬─────────┤
│ id │ email        │ role │ name    │
├────┼──────────────┼──────┼─────────┤
│ 1  │ student@...  │ stu.. │ John   │
│ 2  │ company@...  │ com.. │ ABC Co │
└────┴──────────────┴──────┴─────────┘
```

---

## 💻 **Method 3: Using SQLite Command Line**

For those who like the terminal!

### **Step 1: Open SQLite**
```bash
# Navigate to your project directory
cd D:\Final-Project-main

# Open the database
sqlite3 internship.db
```

### **Step 2: View Tables**
```sql
-- List all tables
.tables

-- See table structure
.schema users

-- View data
SELECT * FROM users;

-- Count rows
SELECT COUNT(*) FROM users;

-- Formatted output
.mode column
.headers on
SELECT * FROM users LIMIT 5;

-- Exit
.quit
```

### **Useful Commands:**
```sql
-- Show all commands
.help

-- Pretty output
.mode box
.headers on

-- Export to CSV
.mode csv
.output users.csv
SELECT * FROM users;
.output stdout

-- Show query execution time
.timer on
```

---

## 🔧 **Method 4: Using Python Interactive Shell**

Quick and simple!

### **Option A: View All Data**
```python
import sqlite3

# Connect
conn = sqlite3.connect('internship.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(dict(user))

conn.close()
```

### **Option B: Specific Queries**
```python
import sqlite3

conn = sqlite3.connect('internship.db')
cursor = conn.cursor()

# Count students
cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
print(f"Students: {cursor.fetchone()[0]}")

# Count internships
cursor.execute("SELECT COUNT(*) FROM internships")
print(f"Internships: {cursor.fetchone()[0]}")

# Get all internship titles
cursor.execute("SELECT title, description FROM internships")
for title, desc in cursor.fetchall():
    print(f"- {title}: {desc[:50]}...")

conn.close()
```

### **Option C: Interactive Exploration**
```bash
python

>>> import sqlite3
>>> conn = sqlite3.connect('internship.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT * FROM users").fetchall()
[(1, 'student@example.com', 'hash...', 'student', 'John', '2025-10-30'), ...]
```

---

## 🎨 **Method 5: VS Code / Cursor Extension**

If you're using VS Code or Cursor IDE:

### **Step 1: Install Extension**
1. Open Extensions (Ctrl+Shift+X)
2. Search for "SQLite" or "SQLite Viewer"
3. Install **SQLite** by alexcvzz (most popular)

### **Step 2: View Database**
1. In VS Code Explorer, find `internship.db`
2. Right-click → **"Open Database"**
3. A new SQLite Explorer panel appears
4. Click on any table to view data

### **Features:**
- ✅ Integrated in your editor
- ✅ View data without leaving IDE
- ✅ Run queries directly
- ✅ Export data

---

## 📊 **Method 6: Quick Data Summary Script**

Want a quick overview? Run this:

```python
import sqlite3

conn = sqlite3.connect('internship.db')
cursor = conn.cursor()

print("DATABASE SUMMARY")
print("=" * 50)

tables = ['users', 'profiles', 'internships', 'applications', 'messages', 'cvs']

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table.capitalize():20} {count:>5} rows")

print("=" * 50)

# Role breakdown
cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
print("\nUser Roles:")
for role, count in cursor.fetchall():
    print(f"  {role.capitalize():15} {count:>3}")

conn.close()
```

**Output:**
```
DATABASE SUMMARY
==================================================
Users                    5 rows
Profiles                 3 rows
Internships             10 rows
Applications             8 rows
Messages                 2 rows
Cvs                      3 rows
==================================================

User Roles:
  Student              3
  Company              1
  Admin                1
```

---

## 🔍 **Common Queries You Might Want**

### **1. View All Students**
```sql
SELECT id, email, name FROM users WHERE role='student';
```

### **2. View All Internships with Company Names**
```sql
SELECT i.title, i.description, u.name as company_name 
FROM internships i 
JOIN users u ON i.company_id = u.id;
```

### **3. View Applications with Student and Internship Info**
```sql
SELECT 
    u.name as student_name,
    i.title as internship_title,
    a.status,
    a.applied_at
FROM applications a
JOIN users u ON a.student_id = u.id
JOIN internships i ON a.internship_id = i.id;
```

### **4. View Student CVs**
```sql
SELECT full_name, email, education, certifications 
FROM cvs;
```

### **5. View Messages Between Users**
```sql
SELECT 
    s.name as sender,
    r.name as receiver,
    m.content,
    m.sent_at
FROM messages m
JOIN users s ON m.sender_id = s.id
JOIN users r ON m.receiver_id = r.id;
```

---

## 🎯 **Recommended Method for You**

Based on your needs:

### **For Quick Look:**
✅ **Use Method 1** - Run `python view_database.py`

### **For Exploring Data:**
✅ **Use Method 2** - DB Browser for SQLite (GUI)

### **For Development:**
✅ **Use Method 5** - VS Code SQLite Extension

### **For Specific Queries:**
✅ **Use Method 3** - SQLite Command Line

---

## 🚀 **Try It Now!**

### **Easiest Way - Run This Now:**

```bash
# Open terminal in project folder
cd D:\Final-Project-main

# Run the viewer script
python view_database.py
```

**OR**

```bash
# Open SQLite directly
sqlite3 internship.db

# Run this query
.mode column
.headers on
SELECT * FROM users;
```

---

## 📸 **What You'll See**

### **Sample Data from Users Table:**
```
┌────┬────────────────────┬──────────┬──────────────┬─────────────────────┐
│ id │ email              │ role     │ name         │ created_at          │
├────┼────────────────────┼──────────┼──────────────┼─────────────────────┤
│ 1  │ student@ex.com     │ student  │ John Doe     │ 2025-10-30 10:00:00 │
│ 2  │ company@ex.com     │ company  │ ABC Corp     │ 2025-10-30 10:01:00 │
│ 3  │ admin@ex.com       │ admin    │ Admin User   │ 2025-10-30 10:02:00 │
└────┴────────────────────┴──────────┴──────────────┴─────────────────────┘
```

### **Sample Data from Internships Table:**
```
┌────┬────────────────────────┬──────────────────────┬─────────────────┐
│ id │ title                  │ company_id           │ required_skills │
├────┼────────────────────────┼──────────────────────┼─────────────────┤
│ 1  │ Python Developer       │ 2                    │ Python, Flask   │
│ 2  │ Web Developer          │ 2                    │ HTML, CSS, JS   │
└────┴────────────────────────┴──────────────────────┴─────────────────┘
```

---

## 🔒 **Important Notes**

### **Password Security:**
- Passwords are **hashed** - you'll see something like:
  ```
  pbkdf2:sha256:260000$abc123$def456...
  ```
- This is normal and secure!
- You can't "unhash" them (that's the point!)

### **Database Safety:**
- The `view_database.py` script is **read-only**
- DB Browser for SQLite has an edit mode - be careful!
- Always backup before making changes:
  ```bash
  copy internship.db internship_backup.db
  ```

---

## 💡 **Troubleshooting**

### **Problem: "database is locked"**
**Solution:** Close the Flask app first
```bash
# Stop Flask (Ctrl+C)
# Then view database
```

### **Problem: "no such table"**
**Solution:** Make sure you're in the right directory
```bash
cd D:\Final-Project-main
```

### **Problem: "file not found"**
**Solution:** Check if database exists
```bash
dir *.db
# Should show: internship.db
```

---

## ✅ **Quick Start Checklist**

- [ ] Navigate to project folder
- [ ] Run `python view_database.py` for quick overview
- [ ] Download DB Browser for SQLite for detailed exploration
- [ ] Try running some SQL queries
- [ ] Check out your actual data!

---

## 🎓 **Learning SQL?**

Great opportunity to practice!

**Try these queries:**
```sql
-- Count everything
SELECT 
    (SELECT COUNT(*) FROM users) as users,
    (SELECT COUNT(*) FROM internships) as internships,
    (SELECT COUNT(*) FROM applications) as applications;

-- Find most popular internship
SELECT i.title, COUNT(a.id) as application_count
FROM internships i
LEFT JOIN applications a ON i.id = a.internship_id
GROUP BY i.id
ORDER BY application_count DESC
LIMIT 1;

-- Find students with CVs
SELECT u.name, cv.education, cv.certifications
FROM users u
JOIN cvs cv ON u.id = cv.user_id
WHERE u.role = 'student';
```

---

## 📚 **Summary**

**6 Ways to View Your Database:**

1. ✅ **Python Script** (view_database.py) - Run now!
2. ✅ **DB Browser** - Best visual tool
3. ✅ **SQLite CLI** - For terminal lovers
4. ✅ **Python Interactive** - Quick queries
5. ✅ **VS Code Extension** - Integrated viewing
6. ✅ **Custom Scripts** - Tailored queries

**Start with:** `python view_database.py` 🚀

---

**Your database is at:** `D:\Final-Project-main\internship.db`

**Just run:** `python view_database.py` and see everything! 🎉



