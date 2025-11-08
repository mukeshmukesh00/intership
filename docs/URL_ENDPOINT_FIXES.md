# URL Endpoint Fixes for Blueprint Architecture

## Problem
When refactoring the Flask application to use blueprints, the URL endpoints changed from simple names (e.g., `'home'`) to blueprint-prefixed names (e.g., `'main.home'`). However, the templates were still using the old endpoint names, causing `BuildError` exceptions.

## Error Message
```
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'home'. Did you mean 'main.home' instead?
```

## Solution
Updated all template files to use the correct blueprint-prefixed endpoint names.

## Files Fixed

### 1. `templates/components/navbar.html`
**Changes:**
- `url_for('home')` → `url_for('main.home')`
- `url_for('student_dashboard')` → `url_for('student.dashboard')`
- `url_for('internships')` → `url_for('main.internships')`
- `url_for('company_dashboard')` → `url_for('company.dashboard')`
- `url_for('post_internship')` → `url_for('company.post_internship')`
- `url_for('admin_dashboard')` → `url_for('admin.dashboard')`
- `url_for('logout')` → `url_for('auth.logout')`
- `url_for('login')` → `url_for('auth.login')`
- `url_for('register')` → `url_for('auth.register')`

### 2. `templates/register.html`
**Changes:**
- `url_for('register')` → `url_for('auth.register')`
- `url_for('login')` → `url_for('auth.login')`

### 3. `templates/login.html`
**Changes:**
- `url_for('login')` → `url_for('auth.login')`
- `url_for('register')` → `url_for('auth.register')`

### 4. `templates/internships.html`
**Changes:**
- `url_for('apply_internship', ...)` → `url_for('student.apply_internship', ...)`
- `url_for('login')` → `url_for('auth.login')`

### 5. `templates/company_dashboard.html`
**Changes:**
- `url_for('post_internship')` → `url_for('company.post_internship')`

### 6. `templates/index.html`
**Changes:**
- `url_for('register')` → `url_for('auth.register')`
- `url_for('login')` → `url_for('auth.login')`
- `url_for('student_dashboard')` → `url_for('student.dashboard')`
- `url_for('company_dashboard')` → `url_for('company.dashboard')`
- `url_for('admin_dashboard')` → `url_for('admin.dashboard')`

### 7. `templates/student_profile.html`
**Changes:**
- `url_for('select_skills')` → `url_for('student.select_skills')`

## Blueprint Endpoint Mapping

| Old Endpoint | New Endpoint | Blueprint |
|--------------|--------------|-----------|
| `home` | `main.home` | main |
| `login` | `auth.login` | auth |
| `register` | `auth.register` | auth |
| `logout` | `auth.logout` | auth |
| `student_dashboard` | `student.dashboard` | student |
| `select_skills` | `student.select_skills` | student |
| `student_profile` | `student.profile` | student |
| `apply_internship` | `student.apply_internship` | student |
| `company_dashboard` | `company.dashboard` | company |
| `post_internship` | `company.post_internship` | company |
| `update_application` | `company.update_application` | company |
| `admin_dashboard` | `admin.dashboard` | admin |
| `delete_user` | `admin.delete_user` | admin |
| `delete_internship` | `admin.delete_internship` | admin |
| `internships` | `main.internships` | main |
| `send_message` | `messaging.send_message` | messaging |
| `cv.create` | `cv.create` | cv |
| `cv.edit` | `cv.edit` | cv |
| `cv.view` | `cv.view` | cv |
| `cv.delete` | `cv.delete` | cv |

## Testing
After applying these fixes:
1. The application starts without URL build errors
2. All navigation links work correctly
3. Forms submit to the correct endpoints
4. The CV creation feature is fully functional

## Prevention
When adding new routes in blueprints:
1. Always use the blueprint-prefixed endpoint names in templates
2. Test all URL generation with `url_for()` calls
3. Use consistent naming conventions across blueprints
4. Document endpoint mappings for future reference

## Status
✅ **FIXED** - All URL endpoint errors resolved. Application is now fully functional with the blueprint architecture.
