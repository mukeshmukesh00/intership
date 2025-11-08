#!/usr/bin/env python3
"""
Migration script to help transition from monolithic app.py to blueprint structure.
This script backs up the original app.py and replaces it with the new blueprint version.
"""

import shutil
import os
from datetime import datetime

def backup_original_app():
    """Create a backup of the original app.py"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"app_original_backup_{timestamp}.py"
    
    if os.path.exists("app.py"):
        shutil.copy2("app.py", backup_name)
        print(f"✅ Backed up original app.py to {backup_name}")
        return True
    else:
        print("❌ app.py not found")
        return False

def replace_app():
    """Replace app.py with the new blueprint version"""
    if os.path.exists("app_new.py"):
        shutil.copy2("app_new.py", "app.py")
        print("✅ Replaced app.py with blueprint version")
        return True
    else:
        print("❌ app_new.py not found")
        return False

def main():
    print("🔄 Migrating to Blueprint Architecture...")
    print("=" * 50)
    
    # Step 1: Backup original
    if not backup_original_app():
        return
    
    # Step 2: Replace with new version
    if not replace_app():
        return
    
    print("=" * 50)
    print("✅ Migration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Test the application: python app.py")
    print("2. Verify all functionality works as expected")
    print("3. The original app.py has been backed up with timestamp")
    print("4. You can now use the new blueprint structure")
    print("\n📁 New structure:")
    print("- blueprints/ - Contains all route modules")
    print("- utils/ - Contains utility functions")
    print("- app.py - Now uses blueprints (refactored)")

if __name__ == "__main__":
    main()
