# Database Information

## 🗄️ **Database Used: SQLite3**

---

## 📊 **Quick Summary**

| Property | Value |
|----------|-------|
| **Database Type** | SQLite3 |
| **Database File** | `internship.db` |
| **Library** | `sqlite3` (Python built-in) |
| **Connection** | File-based (no server) |
| **Size** | Small (~few MB) |

---

## 🔍 **What is SQLite?**

**SQLite** is a **lightweight, file-based relational database**.

### **Key Characteristics:**

✅ **File-Based**
- Entire database stored in a single file (`internship.db`)
- No separate database server needed
- Easy to backup (just copy the file)

✅ **Serverless**
- No installation required
- No configuration needed
- No process to start/stop

✅ **Self-Contained**
- Built into Python (no pip install needed)
- Zero dependencies
- Works out of the box

✅ **ACID Compliant**
- Atomicity: Transactions complete or rollback
- Consistency: Data stays valid
- Isolation: Concurrent operations don't interfere
- Durability: Committed data survives crashes

---

## 📁 **Database Files in This Project**

### **1. internship.db** (Main Database)
```
Location: D:\Final-Project-main\internship.db
Purpose: Stores all application data
```

### **2. app.db** (Old/Backup?)
```
Location: D:\Final-Project-main\app.db
Purpose: Possibly from earlier version (not used)
```

**Active Database:** `internship.db` ✅

---

## ⚙️ **How It's Configured**

### **In app_new.py (Line 19):**
```python
app.config['DATABASE'] = 'internship.db'
```

### **Connection Code (utils/database.py):**
```python
import sqlite3
from flask import current_app

def init_db():
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        # Create tables...
```

### **Get Database Connection:**
```python
def get_db():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn
```

---

## 📊 **Database Schema (Tables)**

The database contains **6 tables**:

### **1. users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'company', 'admin')),
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Purpose:** Stores all user accounts (students, companies, admins)

---

### **2. profiles**
```sql
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skills TEXT,
    education TEXT,
    experience TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```
**Purpose:** Stores student profile information

---

### **3. internships**
```sql
CREATE TABLE internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    required_skills TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES users (id)
)
```
**Purpose:** Stores internship postings from companies

---

### **4. applications**
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    internship_id INTEGER NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES users (id),
    FOREIGN KEY (internship_id) REFERENCES internships (id)
)
```
**Purpose:** Tracks student applications to internships

---

### **5. messages**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    internship_id INTEGER NOT NULL,
    content TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id),
    FOREIGN KEY (internship_id) REFERENCES internships (id)
)
```
**Purpose:** Stores messages between students and companies

---

### **6. cvs**
```sql
CREATE TABLE cvs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    linkedin_url TEXT,
    github_url TEXT,
    objective TEXT,
    education TEXT,
    education_details TEXT,
    work_experience TEXT,
    projects TEXT,
    certifications TEXT,
    languages TEXT,
    languages_details TEXT,
    interests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```
**Purpose:** Stores student CV/resume information

---

## 🔗 **Database Relationships**

```
users (1) ──────── (many) profiles
  │
  ├─────── (many) internships (as company)
  │
  ├─────── (many) applications (as student)
  │
  ├─────── (many) messages (as sender/receiver)
  │
  └─────── (many) cvs

internships (1) ── (many) applications
     │
     └──────────── (many) messages

applications ───── links students to internships
```

---

## 💾 **Data Storage**

### **Text Storage:**
- Skills stored as comma-separated strings: `"Python, JavaScript, React"`
- Descriptions stored as plain text
- Dates stored as TEXT in ISO format: `"2025-10-30 12:34:56"`

### **File Location:**
```
D:\Final-Project-main\internship.db
```

### **File Size:**
- Empty: ~20 KB
- With sample data: ~50-200 KB
- After usage: Depends on data (typically < 5 MB)

---

## 🔍 **How to View the Database**

### **Method 1: SQLite Browser (GUI)**
1. Download **DB Browser for SQLite** (free)
2. Open `internship.db`
3. Browse tables, data, run queries

### **Method 2: Command Line**
```bash
sqlite3 internship.db

.tables              # List all tables
.schema users        # Show users table structure
SELECT * FROM users; # Query data
.quit                # Exit
```

### **Method 3: Python**
```python
import sqlite3

conn = sqlite3.connect('internship.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print(users)
```

---

## ⚡ **Advantages of SQLite for This Project**

### **1. Simplicity**
✅ No server setup
✅ No configuration
✅ Works immediately

### **2. Portability**
✅ Single file database
✅ Easy to backup (copy file)
✅ Easy to move/share

### **3. Zero Cost**
✅ Free
✅ Open source
✅ No licensing

### **4. Perfect for Development**
✅ Fast for small datasets
✅ Easy debugging
✅ Built into Python

### **5. No Dependencies**
✅ No external database server
✅ No network latency
✅ Works offline

---

## ⚠️ **Limitations of SQLite**

### **When SQLite is NOT Good:**

❌ **High Concurrency**
- Limited concurrent writes
- Not ideal for 1000+ simultaneous users

❌ **Very Large Databases**
- Works best under 1 GB
- Slower than PostgreSQL/MySQL for huge datasets

❌ **Client-Server Architecture**
- Can't connect from multiple machines
- All users must access same file

❌ **Advanced Features**
- No stored procedures
- Limited user management
- No role-based access control

**BUT:** For this internship project, SQLite is perfect! ✅

---

## 🔄 **Database Operations in This Project**

### **CREATE (Insert Data):**
```python
cursor.execute(
    "INSERT INTO users (email, password, role, name) VALUES (?, ?, ?, ?)",
    ('student@example.com', 'hashed_password', 'student', 'John Doe')
)
conn.commit()
```

### **READ (Query Data):**
```python
cursor.execute("SELECT * FROM internships WHERE company_id=?", (company_id,))
internships = cursor.fetchall()
```

### **UPDATE (Modify Data):**
```python
cursor.execute(
    "UPDATE applications SET status=? WHERE id=?",
    ('accepted', application_id)
)
conn.commit()
```

### **DELETE (Remove Data):**
```python
cursor.execute("DELETE FROM internships WHERE id=?", (internship_id,))
conn.commit()
```

---

## 🔒 **Data Security**

### **Passwords:**
- Stored as **hashed** (using Werkzeug)
- Never stored in plain text
- Example: `pbkdf2:sha256:260000$salt$hash`

### **SQL Injection Prevention:**
- Uses **parameterized queries** (?)
- Never concatenates SQL strings
- Example: `"SELECT * FROM users WHERE email=?"` ✅

### **File Security:**
- Database file has standard file permissions
- Should not be accessible via web server
- Typically not committed to Git

---

## 📈 **Database Performance**

### **Optimizations Used:**

✅ **Indexes on Primary Keys**
- Automatic on `id` fields
- Fast lookups

✅ **Foreign Keys**
- Maintains data integrity
- Cascading deletes possible

✅ **Row Factory**
```python
conn.row_factory = sqlite3.Row
```
- Returns rows as dictionaries
- Easier to work with

---

## 🔧 **Backup & Restore**

### **Backup (Simple):**
```bash
# Just copy the file!
copy internship.db internship_backup.db
```

### **Backup (SQL Export):**
```bash
sqlite3 internship.db .dump > backup.sql
```

### **Restore:**
```bash
sqlite3 new_database.db < backup.sql
```

---

## 📊 **Database Statistics**

**Current Database (`internship.db`):**

| Table | Columns | Purpose |
|-------|---------|---------|
| users | 6 | User accounts |
| profiles | 5 | Student profiles |
| internships | 6 | Job postings |
| applications | 5 | Student applications |
| messages | 6 | Communication |
| cvs | 17 | Student resumes |

**Total Tables:** 6  
**Total Foreign Keys:** 8  
**Supports:** CRUD operations, Relationships, Transactions

---

## 🆚 **SQLite vs Other Databases**

| Feature | SQLite | MySQL | PostgreSQL |
|---------|--------|-------|------------|
| **Server** | ❌ No | ✅ Yes | ✅ Yes |
| **Setup** | ✅ Easy | ⚠️ Medium | ⚠️ Medium |
| **File-based** | ✅ Yes | ❌ No | ❌ No |
| **Concurrent Writes** | ⚠️ Limited | ✅ High | ✅ High |
| **Max Size** | ~140 TB | Unlimited | Unlimited |
| **Best For** | Small apps | Web apps | Enterprise |
| **This Project** | ✅ Perfect | Overkill | Overkill |

---

## ✅ **Summary**

### **Database Used:**
```
SQLite3
File: internship.db
Location: D:\Final-Project-main\internship.db
```

### **Why SQLite?**
- ✅ Built into Python
- ✅ No setup required
- ✅ Perfect for small/medium projects
- ✅ Easy to backup and share
- ✅ Fast for this use case

### **Tables:**
- 6 tables (users, profiles, internships, applications, messages, cvs)
- Relational structure with foreign keys
- Stores all application data

### **Access:**
```python
import sqlite3
conn = sqlite3.connect('internship.db')
```

---

**That's the database! Simple, effective, and perfect for this internship recommendation system.** 🗄️



