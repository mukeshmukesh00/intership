# Company Dashboard Buttons - Complete Functionality Guide

## Overview
The company dashboard has two main action buttons for each internship posting:
1. **View Details** - Shows complete internship information
2. **Delete** - Permanently removes the internship and all related data

---

## 1. View Details Button

### What It Does
Opens a modal popup showing complete internship information without leaving the dashboard.

### Information Displayed
- **Full Title**: Complete internship title
- **Complete Description**: Full description (not truncated like in card view)
- **Required Skills**: All skills displayed as professional badges
- **Posted Date**: When the internship was posted
- **Application Count**: Number of applications received

### How to Use
1. Find the internship you want to view
2. Click the **"View Details"** button (blue outline button with eye icon)
3. Modal opens showing all information
4. Click "Close" or click outside modal to dismiss

### Technical Implementation
- **Button Location**: Each internship card footer
- **Action**: Opens Bootstrap modal
- **Data Transfer**: Uses HTML5 data attributes
- **No Page Reload**: Instant display using JavaScript

### Code Flow
```
User clicks "View Details" 
  ↓
JavaScript reads data attributes from button
  ↓
Populates modal with internship data
  ↓
Converts skills to badges
  ↓
Counts applications for this internship
  ↓
Shows modal
```

---

## 2. Delete Button

### What It Does
Permanently deletes an internship posting and all related data from the database.

### What Gets Deleted
When you delete an internship, the following are **permanently removed**:
1. ✅ The internship posting itself
2. ✅ All applications submitted for this internship
3. ✅ All messages related to this internship
4. ✅ All related database records

### How to Use
1. Find the internship you want to delete
2. Click the **"Delete"** button (red outline button with trash icon)
3. **Confirmation modal appears** showing:
   - Internship title
   - Warning about what will be deleted
   - "This action cannot be undone" message
4. Click **"Delete Internship"** to confirm (or "Cancel" to abort)
5. Success message appears
6. Page reloads showing updated internship list

### Safety Features
- **Confirmation Required**: Can't accidentally delete - must confirm
- **Clear Warnings**: Shows exactly what will be deleted
- **Loading State**: Button shows "Deleting..." while processing
- **Success Feedback**: Toast notification confirms deletion
- **Error Handling**: Shows error message if deletion fails

### Technical Implementation

#### Backend Route
```python
@company_bp.route('/internship/<int:internship_id>/delete', methods=['POST'])
def delete_internship(internship_id):
    # Verify ownership
    # Delete messages
    # Delete applications  
    # Delete internship
    # Return JSON response
```

#### Database Operations (in correct order)
1. Verify internship belongs to logged-in company
2. Delete messages (foreign key dependency)
3. Delete applications (foreign key dependency)
4. Delete internship posting
5. Commit transaction

#### JavaScript Flow
```
User clicks "Delete"
  ↓
Show confirmation modal with warnings
  ↓
User clicks "Delete Internship" to confirm
  ↓
AJAX POST request to /company/internship/{id}/delete
  ↓
Backend verifies ownership and deletes data
  ↓
Success response received
  ↓
Show success message
  ↓
Reload page after 1 second
```

---

## Button Locations and Styling

### View Details Button
```html
<button 
  type="button"
  class="btn btn-sm btn-outline-primary view-details"
>
  <i class="fas fa-eye me-1"></i>View Details
</button>
```
- **Color**: Blue outline
- **Icon**: Eye (fa-eye)
- **Position**: Left side of card footer

### Delete Button
```html
<button 
  type="button"
  class="btn btn-sm btn-outline-danger delete-internship"
>
  <i class="fas fa-trash me-1"></i>Delete
</button>
```
- **Color**: Red outline  
- **Icon**: Trash (fa-trash)
- **Position**: Right side of card footer

---

## Complete Feature List

### View Details Modal Features
- ✅ Large modal (modal-lg) for better readability
- ✅ Professional header with internship title
- ✅ Organized sections with icons
- ✅ Skills displayed as badges
- ✅ Real-time application count
- ✅ Responsive design
- ✅ Easy to close

### Delete Functionality Features
- ✅ Two-step confirmation process
- ✅ Clear warning messages
- ✅ Shows what will be deleted
- ✅ Ownership verification (can't delete other company's internships)
- ✅ Cascading delete (removes all related data)
- ✅ Loading state indication
- ✅ Success/error feedback
- ✅ Automatic page refresh

---

## Testing Both Features

### Test View Details
1. Login as a company
2. Navigate to dashboard
3. Find any posted internship
4. Click "View Details"
5. **Expected Result**: Modal opens showing:
   - Complete description
   - All skills as badges
   - Posted date
   - Application count

### Test Delete
1. Login as a company
2. Navigate to dashboard  
3. Find an internship you want to delete
4. Click "Delete"
5. **Expected Result**: Confirmation modal appears
6. Click "Delete Internship"
7. **Expected Result**: 
   - Button shows "Deleting..."
   - Success message appears
   - Page reloads
   - Internship is gone from list

---

## Security Features

### Authorization Checks
- ✅ Must be logged in as company
- ✅ Can only delete own internships
- ✅ Backend verifies ownership before deletion
- ✅ Returns 401 Unauthorized if verification fails

### Data Integrity
- ✅ Foreign key constraints respected
- ✅ Deletion order prevents orphaned records
- ✅ Transaction-based (all or nothing)
- ✅ Error handling for failed deletions

---

## API Endpoints Used

### View Details
- **Method**: Client-side only (no API call)
- **Data Source**: HTML data attributes
- **Performance**: Instant (no network request)

### Delete Internship
- **Endpoint**: `POST /company/internship/{id}/delete`
- **Authentication**: Session-based
- **Request**: JSON
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Internship deleted successfully"
  }
  ```

---

## Troubleshooting

### View Details Not Working
- Check browser console for JavaScript errors
- Ensure jQuery and Bootstrap are loaded
- Verify data attributes are present on button

### Delete Not Working
- Check if you're logged in as company
- Verify you own the internship
- Check browser console for AJAX errors
- Check Flask server logs for backend errors

### Modal Not Closing
- Click outside modal
- Press ESC key
- Click "Close" or "Cancel" button
- Refresh page if stuck

---

## Future Enhancements (Optional)

### View Details
- [ ] Add edit button in modal
- [ ] Show list of applicants
- [ ] Display analytics (views, clicks)
- [ ] Add share functionality

### Delete
- [ ] Soft delete option (archive instead)
- [ ] Undo functionality
- [ ] Export data before deletion
- [ ] Bulk delete multiple internships

---

## Files Involved

### Frontend
- `templates/company_dashboard.html` - Main dashboard with buttons and modals
- Uses jQuery for AJAX and modal control
- Uses Bootstrap for styling and modals

### Backend
- `blueprints/company.py` - Delete route handler
- `utils/database.py` - Database connection utilities

---

## Summary

Both buttons are **fully functional**:

✅ **View Details**: Opens modal with complete internship information  
✅ **Delete**: Permanently removes internship with confirmation

Both features include:
- Professional UI/UX
- Safety confirmations
- Error handling
- Loading states
- Success feedback

**Ready to use!** 🎉

