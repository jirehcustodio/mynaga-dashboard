#!/usr/bin/env python3
"""
Fetch MongoDB IDs from MyNaga API and update Google Sheets Column L
Uses the EXACT SAME approach as the AppScript to fetch report data.

Usage:
    python3 fetch_mynaga_ids.py [spreadsheet_id] [start_date] [end_date]
    
    spreadsheet_id: Your Google Spreadsheet ID (required)
    start_date: Start date YYYY-MM-DD (optional, default: Aug 1 of current year)
    end_date: End date YYYY-MM-DD (optional, default: last day of current month)
"""

import asyncio
import aiohttp
import sys
from datetime import datetime, timedelta

# Check if spreadsheet ID provided
if len(sys.argv) < 2:
    print("❌ Error: Spreadsheet ID required")
    print("\nUsage:")
    print("  python3 fetch_mynaga_ids.py SPREADSHEET_ID [START_DATE] [END_DATE]")
    print("\nExample:")
    print("  python3 fetch_mynaga_ids.py 1AbC123XyZ 2025-08-01 2025-10-31")
    sys.exit(1)

SPREADSHEET_ID = sys.argv[1]
SHEET_NAME = 'Main'  # The main sheet name

try:
    from google_sheets_auth import GoogleSheetsAuthenticator
except ImportError:
    print("❌ Could not import GoogleSheetsAuthenticator")
    print("   Make sure google_sheets_auth.py exists")
    sys.exit(1)

# MyNaga API Configuration (MATCHES AppScript)
MYNAGA_API_BASE = "https://mynaga.app/api/reports"
# TODO: Update this token (expires ~Feb 2026)
MYNAGA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OGE0ODk3Zjg1ZmIxYTdiYjU2YTNjYTQiLCJpYXQiOjE3NjA1ODE1NDgsImV4cCI6MTc2MTE4NjM0OH0.AlIem843s3R_SaGLQVMjP3EfYaVMrOKANoVYv7zX3ns"

# AppScript's fixed query parameters
FIXED_QUERY_PARAMS = "filter_cancel=1&sortQuery=%7B%22priority%22:-1,%22status%22:1,%22date_created%22:1%7D"

async def fetch_mynaga_reports(start_date=None, end_date=None):
    """
    Fetch all reports from MyNaga API using the SAME method as AppScript.
    
    Args:
        start_date: Start date (YYYY-MM-DD) or None for default (Aug 1, current year)
        end_date: End date (YYYY-MM-DD) or None for default (last day of current month)
    """
    print("🔍 Fetching reports from MyNaga API...")
    print(f"   Using AppScript-compatible approach...")
    
    # Default dates (matches AppScript's showSidebar function)
    now = datetime.now()
    if not start_date:
        start_date = f"{now.year}-08-01"  # Aug 1 of current year
    if not end_date:
        # Last day of current month
        next_month = now.month % 12 + 1
        year = now.year if now.month < 12 else now.year + 1
        last_day = datetime(year, next_month, 1) - timedelta(days=1)
        end_date = last_day.strftime("%Y-%m-%d")
    
    # Convert to ISO format (matches AppScript)
    start_datetime = datetime.fromisoformat(f"{start_date}T00:00:00")
    end_datetime = datetime.fromisoformat(f"{end_date}T23:59:59.999")
    
    from_date = start_datetime.isoformat() + 'Z'
    to_date = end_datetime.isoformat() + 'Z'
    
    # Build URL exactly like AppScript
    date_params = f"date_created_from={from_date}&date_created_to={to_date}"
    full_api_url = f"{MYNAGA_API_BASE}?{date_params}&{FIXED_QUERY_PARAMS}"
    
    print(f"   Date Range: {start_date} to {end_date}")
    print(f"   API URL: {full_api_url}")
    
    headers = {
        "Authorization": f"Bearer {MYNAGA_TOKEN}",
        "Accept": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            print(f"   Fetching...")
            async with session.get(full_api_url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if isinstance(data, list):
                        reports = data
                    elif isinstance(data, dict):
                        # Check for error messages
                        if data.get('message') == 'Unauthenticated.':
                            print(f"❌ Authentication failed. Token might be expired.")
                            return None
                        reports = data.get('data', data.get('reports', []))
                    else:
                        print(f"❌ Unexpected response format")
                        return None
                    
                    print(f"✅ Fetched {len(reports)} reports from MyNaga API")
                    return reports
                    
                elif response.status == 401:
                    print(f"❌ Unauthorized (401). Token expired or invalid.")
                    print(f"   Get a fresh token from MyNaga admin panel")
                    return None
                else:
                    error_text = await response.text()
                    print(f"❌ API returned status {response.status}")
                    print(f"   Response: {error_text[:200]}")
                    return None
                    
        except asyncio.TimeoutError:
            print(f"❌ Request timed out after 30 seconds")
            return None
        except Exception as e:
            print(f"❌ Error fetching from API: {e}")
            return None

def create_control_to_id_map(reports):
    """
    Create mapping from control_no to MongoDB _id
    Uses the SAME field names as AppScript: control_number and _id
    """
    print("\n📋 Creating control_no → _id mapping...")
    
    mapping = {}
    for report in reports:
        # AppScript uses: report.control_number and report._id
        control_no = report.get('control_number', '').strip()
        mongo_id = report.get('_id', '').strip()
        
        if control_no and mongo_id:
            # Create URL exactly like AppScript
            url = f"https://mynaga.app/reports?_id={mongo_id}"
            mapping[control_no] = url
            print(f"  ✓ {control_no} → {url}")
        elif control_no:
            print(f"  ⚠️  {control_no} has no _id")
        elif mongo_id:
            print(f"  ⚠️  Report has _id but no control_number: {mongo_id}")
    
    print(f"\n✅ Mapped {len(mapping)} reports")
    return mapping

def update_google_sheets(mapping):
    """Update Column L in Google Sheets with MyNaga URLs"""
    print("\n📊 Updating Google Sheets...")
    
    try:
        gs_auth = GoogleSheetsAuthenticator()
        
        # Read current data
        print("  Reading current data...")
        result = gs_auth.read_sheet(SPREADSHEET_ID, f'{SHEET_NAME}!A2:L')
        
        if not result or 'values' not in result:
            print("  No data found in sheet")
            return 0
        
        rows = result.get('values', [])
        print(f"  Found {len(rows)} rows")
        
        # Prepare updates
        updates_to_write = []
        updated_count = 0
        
        for i, row in enumerate(rows):
            if len(row) < 1:
                continue
            
            # Assuming control_no is in column A (index 0)
            control_no = row[0] if len(row) > 0 else None
            
            if control_no and control_no in mapping:
                new_url = mapping[control_no]
                
                # Only update if current value is "Link" or empty
                current_link = row[11] if len(row) > 11 else ''
                if current_link in ['Link', '']:
                    # Store row number and new value
                    updates_to_write.append((i + 2, new_url))  # +2 for header and 0-index
                    updated_count += 1
                    print(f"  ✓ Row {i+2}: {control_no}")
        
        if updates_to_write:
            # Update each cell
            print(f"\n📤 Updating {len(updates_to_write)} cells...")
            for row_num, url in updates_to_write:
                range_name = f'{SHEET_NAME}!L{row_num}'
                gs_auth.write_to_sheet(SPREADSHEET_ID, range_name, [[url]])
            
            print(f"\n✅ Successfully updated {updated_count} rows in Google Sheets!")
        else:
            print("\n⚠️  No rows needed updating (all links already present)")
        
        return updated_count
        
    except Exception as e:
        print(f"\n❌ Error updating Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return 0

async def main():
    """Main execution flow"""
    print("=" * 60)
    print("MyNaga ID Fetcher - Google Sheets Updater")
    print("Using AppScript-compatible API method")
    print("=" * 60)
    
    # Get date range from arguments
    start_date = sys.argv[2] if len(sys.argv) > 2 else None
    end_date = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Step 1: Fetch reports from MyNaga (like AppScript does)
    reports = await fetch_mynaga_reports(start_date, end_date)
    if not reports:
        print("\n❌ Failed to fetch reports from MyNaga API")
        print("\nTroubleshooting:")
        print("1. Check if the token is still valid")
        print("2. Get a fresh token from MyNaga admin panel (F12 → Network → Copy Bearer token)")
        print("3. Update MYNAGA_TOKEN at the top of this script")
        print("4. Make sure date range is valid")
        sys.exit(1)
    
    # Step 2: Create control_no → URL mapping
    mapping = create_control_to_id_map(reports)
    if not mapping:
        print("\n❌ No valid mappings found")
        print("   Check if the API response contains 'control_number' and '_id' fields")
        sys.exit(1)
    
    # Step 3: Update Google Sheets
    updated = update_google_sheets(mapping)
    
    print("\n" + "=" * 60)
    print("✨ Done!")
    print(f"   Reports fetched: {len(reports)}")
    print(f"   Mappings created: {len(mapping)}")
    print(f"   Rows updated: {updated}")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("   1. Check your Google Sheet - Column L should have MyNaga URLs")
    print("   2. Dashboard will auto-sync in 10 seconds")
    print("   3. Click any case → 'View in MyNaga App' button should appear")
    print("   4. Click button → Opens correct MyNaga report! 🎉")

if __name__ == "__main__":
    asyncio.run(main())
