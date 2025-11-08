# Flask Application with Blueprints

This Flask application has been refactored to use blueprints for better maintainability and organization.

## Project Structure

```
├── app.py                 # Original monolithic application
├── app_new.py            # New refactored application using blueprints
├── requirements.txt      # Python dependencies
├── blueprints/           # Blueprint modules
│   ├── __init__.py
│   ├── main.py          # General routes (home, internships)
│   ├── auth.py          # Authentication routes (login, register, logout)
│   ├── student.py       # Student-specific routes
│   ├── company.py       # Company-specific routes
│   ├── admin.py         # Admin-specific routes
│   └── messaging.py     # Messaging functionality
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── database.py      # Database utilities
│   ├── auth.py          # Authentication utilities
│   └── recommendations.py # Recommendation algorithms
├── templates/           # HTML templates
├── static/             # Static files (CSS, JS)
└── internship.db       # SQLite database
```

## Benefits of Blueprint Architecture

1. **Modularity**: Each blueprint handles a specific functionality
2. **Maintainability**: Easier to locate and modify specific features
3. **Scalability**: Easy to add new features or modify existing ones
4. **Team Development**: Multiple developers can work on different blueprints
5. **Testing**: Each blueprint can be tested independently
6. **Code Reusability**: Blueprints can be reused across different applications

## Blueprint Organization

### Main Blueprint (`blueprints/main.py`)
- Home page
- Internship browsing
- General public routes

### Auth Blueprint (`blueprints/auth.py`)
- User registration
- User login
- User logout
- Authentication logic

### Student Blueprint (`blueprints/student.py`)
- Student dashboard
- Profile management
- Skill selection
- Internship applications

### Company Blueprint (`blueprints/company.py`)
- Company dashboard
- Internship posting
- Application management
- Company-specific features

### Admin Blueprint (`blueprints/admin.py`)
- Admin dashboard
- User management
- System administration
- Data management

### Messaging Blueprint (`blueprints/messaging.py`)
- Message sending
- Communication features

## How to Run

### Option 1: Use the new refactored application
```bash
python app_new.py
```

### Option 2: Use the original application
```bash
python app.py
```

Both applications provide the same functionality, but `app_new.py` uses the blueprint architecture.

## Default Login Credentials

- **Admin**: admin@internhub.com / admin123
- **Student**: student@example.com / student123
- **Company**: company@example.com / company123

## Adding New Features

To add new features:

1. Create a new blueprint in the `blueprints/` directory
2. Define routes in the blueprint
3. Register the blueprint in `app_new.py`
4. Add any utility functions to the `utils/` directory

## Database

The application uses SQLite and automatically creates the database with sample data on first run.
