#!/usr/bin/env python3
"""
Manual CSV/Excel import tool for MyNaga URLs
Use this if the API is not accessible

Instructions:
1. Export data from MyNaga with: Control Number, MongoDB _id
2. Save as CSV (mynaga_ids.csv) in this directory
3. Run this script to update Column L in Google Sheets
"""

import csv
import sys
from google_sheets_auth import get_sheets_service
from config import SPREADSHEET_ID, SHEET_NAME

def read_mynaga_csv(filename='mynaga_ids.csv'):
    """Read MyNaga IDs from CSV file"""
    print(f"📂 Reading {filename}...")
    
    mapping = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Try to detect column names
            fieldnames = reader.fieldnames
            print(f"   Columns found: {fieldnames}")
            
            # Find control_no and _id columns (case-insensitive)
            control_col = None
            id_col = None
            
            for field in fieldnames:
                field_lower = field.lower()
                if any(x in field_lower for x in ['control', 'case', 'number', 'no']):
                    control_col = field
                if '_id' in field_lower or 'mongoid' in field_lower or field_lower == 'id':
                    id_col = field
            
            if not control_col or not id_col:
                print(f"❌ Could not find control_no and _id columns")
                print(f"   Expected columns like: control_no, _id")
                print(f"   Found: {fieldnames}")
                return None
            
            print(f"   Using: {control_col} → {id_col}")
            
            for row in reader:
                control_no = row.get(control_col, '').strip()
                mongo_id = row.get(id_col, '').strip()
                
                if control_no and mongo_id:
                    mapping[control_no] = mongo_id
            
            print(f"✅ Loaded {len(mapping)} mappings from CSV")
            return mapping
            
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        print("\n📝 Please create a CSV file with MyNaga data:")
        print("   Format: control_no,_id")
        print("   Example:")
        print("   control_no,_id")
        print("   OTH-251022-2523,68f8cce4fb16457f30003544")
        print("   DRK-250818-001,67123abc45def67890123456")
        return None
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None

def update_google_sheets_from_csv(mapping):
    """Update Column L in Google Sheets"""
    print("\n📊 Updating Google Sheets...")
    
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        # Read current data
        print("  Reading current sheet data...")
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A2:L'
        ).execute()
        
        rows = result.get('values', [])
        print(f"  Found {len(rows)} rows in sheet")
        
        # Prepare batch update
        updates = []
        updated_count = 0
        skipped_count = 0
        
        for i, row in enumerate(rows):
            if len(row) < 1:
                continue
            
            control_no = row[0].strip() if row[0] else None
            
            if control_no in mapping:
                mongo_id = mapping[control_no]
                new_url = f"https://mynaga.app/reports?_id={mongo_id}"
                
                # Check current value in Column L (index 11)
                current_link = row[11].strip() if len(row) > 11 else ''
                
                # Only update if "Link" or empty
                if current_link in ['Link', '', 'link']:
                    updates.append({
                        'range': f'{SHEET_NAME}!L{i+2}',
                        'values': [[new_url]]
                    })
                    updated_count += 1
                    print(f"  ✓ Row {i+2}: {control_no}")
                else:
                    skipped_count += 1
                    print(f"  ⊘ Row {i+2}: {control_no} (already has URL)")
        
        if updates:
            print(f"\n📤 Updating {len(updates)} cells in Google Sheets...")
            
            # Batch update
            body = {
                'valueInputOption': 'RAW',
                'data': updates
            }
            result = sheet.values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()
            
            print(f"\n✅ Success!")
            print(f"   Updated: {updated_count} rows")
            print(f"   Skipped: {skipped_count} rows (already had URLs)")
            print(f"   Total cells updated: {result.get('totalUpdatedCells', 0)}")
            return True
        else:
            print(f"\n⚠️  No updates needed")
            print(f"   All {len(rows)} rows already have URLs")
            return False
            
    except Exception as e:
        print(f"\n❌ Error updating Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main execution"""
    print("=" * 70)
    print("MyNaga URL Updater - Manual CSV Import")
    print("=" * 70)
    print()
    
    # Check if CSV file exists
    csv_file = 'mynaga_ids.csv'
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    # Read CSV
    mapping = read_mynaga_csv(csv_file)
    if not mapping:
        print("\n" + "=" * 70)
        print("❌ Could not load MyNaga IDs")
        print("=" * 70)
        return
    
    # Show sample
    print("\n📋 Sample mappings:")
    for i, (control_no, mongo_id) in enumerate(list(mapping.items())[:5]):
        print(f"   {control_no} → https://mynaga.app/reports?_id={mongo_id}")
    if len(mapping) > 5:
        print(f"   ... and {len(mapping) - 5} more")
    
    # Confirm
    print("\n⚠️  This will update Column L in your Google Sheet")
    response = input("Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    # Update
    success = update_google_sheets_from_csv(mapping)
    
    print("\n" + "=" * 70)
    if success:
        print("✨ Done! Check your Google Sheet - Column L should be updated")
        print("   Dashboard will auto-sync in 10 seconds")
        print("   Then 'View in MyNaga App' buttons will appear! 🎉")
    else:
        print("⚠️  Update not completed. Check errors above.")
    print("=" * 70)

if __name__ == "__main__":
    main()
