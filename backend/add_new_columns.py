"""Add new columns to cases table for Google Sheets sync."""
import sqlite3

def add_columns():
    """Add cluster, office, and updates_sent_to_user columns."""
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(cases)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add cluster column (Column D in Google Sheets)
    if 'cluster' not in columns:
        print("Adding 'cluster' column...")
        cursor.execute("ALTER TABLE cases ADD COLUMN cluster VARCHAR(255)")
        print("✅ Added 'cluster' column")
    else:
        print("'cluster' column already exists")
    
    # Add office column (Column I in Google Sheets)
    if 'office' not in columns:
        print("Adding 'office' column...")
        cursor.execute("ALTER TABLE cases ADD COLUMN office VARCHAR(255)")
        print("✅ Added 'office' column")
    else:
        print("'office' column already exists")
    
    # Modify updates_sent_to_user from Boolean to Text (Column N in Google Sheets)
    # SQLite doesn't support ALTER COLUMN, so we'll create a new column if needed
    if 'updates_sent_to_user' in columns:
        # Check the type
        cursor.execute("SELECT typeof(updates_sent_to_user) FROM cases LIMIT 1")
        result = cursor.fetchone()
        if result and result[0] == 'integer':
            print("Converting 'updates_sent_to_user' from Boolean to Text...")
            # Create temporary column
            cursor.execute("ALTER TABLE cases ADD COLUMN updates_sent_to_user_new TEXT")
            # Copy data (convert 1/0 to empty string)
            cursor.execute("UPDATE cases SET updates_sent_to_user_new = '' WHERE updates_sent_to_user = 1")
            # Note: SQLite doesn't allow dropping columns easily, so we'll just use the new column
            print("✅ Added 'updates_sent_to_user_new' column (use this instead)")
            print("   Note: You may need to recreate the database for a clean schema")
    
    conn.commit()
    conn.close()
    print("\n✅ Database migration completed!")
    print("\nNew columns added:")
    print("- cluster (VARCHAR 255) - Column D in Google Sheets")
    print("- office (VARCHAR 255) - Column I in Google Sheets")
    print("- updates_sent_to_user (TEXT) - Column N in Google Sheets (auto-response message)")

if __name__ == "__main__":
    add_columns()
