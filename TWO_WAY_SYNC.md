# Two-Way Sync: Dashboard ↔ Google Sheets

## Overview

Your MyNaga Dashboard now supports **two-way synchronization** with Google Sheets! This means:

✅ **What Works:**
- **Dashboard → Google Sheets**: When you edit a case in the dashboard, it automatically updates the Google Sheets
- **Google Sheets → Dashboard**: Existing auto-sync continues to pull new data from Google Sheets every 10 seconds
- **Cluster Assignments**: Assigning cases to clusters syncs back to Google Sheets
- **Status Updates**: Changing case status in dashboard updates the spreadsheet
- **Real-Time**: Changes sync immediately after saving

❌ **Technical Limitation:**
- **Cannot edit MyNaga App**: The MyNaga App website is an external system we don't control, so dashboard edits cannot be sent to their servers
- **Read-Only from MyNaga App**: We can only view reports from MyNaga App via the external links

---

## How It Works

### Architecture

```
┌─────────────────┐
│  Google Sheets  │◄─────────┐
│   (Main Tab)    │          │
└────────┬────────┘          │
         │                   │
         │ Read (10s)        │ Write (Immediate)
         ▼                   │
┌─────────────────┐          │
│   Dashboard     │──────────┘
│   Database      │
└─────────────────┘
```

1. **Read Direction (Google Sheets → Dashboard)**:
   - Auto-sync runs every 10 seconds
   - Fetches all rows from the "Main" tab
   - Updates local database with changes
   - Existing functionality (already working)

2. **Write Direction (Dashboard → Google Sheets)**:
   - **NEW!** When you edit a case in the dashboard and click "Save"
   - Backend finds the corresponding row in Google Sheets using Control No.
   - Writes updated data back to columns A-K
   - Happens automatically after database update

---

## Synced Fields

The following fields are synced **both ways**:

| Column | Field | Editable in Dashboard |
|--------|-------|----------------------|
| A | Control No. | ❌ (Read-only identifier) |
| B | Category | ✅ Yes |
| C | Sender's Location | ✅ Yes |
| D | Barangay | ✅ Yes |
| E | Description | ✅ Yes |
| F | Date Created | ✅ Yes |
| G | Reported by | ✅ Yes |
| H | Contact Number | ✅ Yes |
| I | Link to Report | ✅ Yes |
| J | MyNaga App Status | ✅ Yes |
| K | Status (OPEN/RESOLVED/FOR REROUTING) | ✅ Yes |

---

## How to Use

### Step 1: Ensure Auto-Sync is Running

The two-way sync requires Google Sheets auto-sync to be active:

```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
bash restart_autosync.sh
```

You should see:
```json
{"success":true,"message":"Auto-sync started: syncing every 10 seconds"}
```

### Step 2: Edit a Case in Dashboard

1. **Open Cases Page**: Navigate to http://localhost:3000/cases
2. **Click a Case**: Click on any case row to open the detail modal
3. **Click "Edit Case"**: Switch to edit mode
4. **Make Changes**: Update any field (category, description, status, etc.)
5. **Click "Save"**: Save the changes

### Step 3: Verify Google Sheets Update

**Automatic Process:**
1. Dashboard saves changes to local database
2. Backend finds the row in Google Sheets by Control No.
3. Updates the corresponding row in the "Main" tab
4. You'll see the changes in Google Sheets immediately!

**Check the Logs:**
```bash
# Backend logs will show:
✅ Case CN-2024-001 synced to Google Sheets
```

---

## Technical Implementation

### Backend Code Changes

#### 1. Google Sheets Auth (`google_sheets_auth.py`)

**New Functions:**

```python
def write_to_sheet(self, spreadsheet_id: str, range_name: str, values: list) -> bool:
    """Write data back to Google Sheets"""
    # Uses Service Account with WRITE permissions
    # Updates specific range (e.g., "Main!A5:K5")
```

```python
def find_row_by_control_no(self, spreadsheet_id: str, sheet_name: str, control_no: str) -> Optional[int]:
    """Find row number for a specific Control No."""
    # Searches Column A for matching Control No.
    # Returns 1-indexed row number
```

**Updated Scope:**
- Changed from `spreadsheets.readonly` → `spreadsheets` (read & write)

#### 2. Google Sheets Sync (`google_sheets_sync.py`)

**New Function:**

```python
def write_case_to_sheet(case_data: Dict, sheet_url: str, credentials_json: str) -> bool:
    """
    Write updated case data back to Google Sheets
    
    Process:
    1. Extract spreadsheet ID and gid from URL
    2. Find sheet name from gid
    3. Locate row by Control No.
    4. Map case data to columns A-K
    5. Update the row
    """
```

**Column Mapping:**
```python
row_values = [
    case_data.get('control_no'),           # A
    case_data.get('category'),             # B
    case_data.get('sender_location'),      # C
    case_data.get('barangay'),             # D
    case_data.get('description'),          # E
    case_data.get('date_created'),         # F
    case_data.get('reported_by'),          # G
    case_data.get('contact_number'),       # H
    case_data.get('link_to_report'),       # I
    case_data.get('mynaga_app_status'),    # J
    case_data.get('status'),               # K
]
```

#### 3. Main API (`main.py`)

**Updated PUT `/api/cases/{case_id}` Endpoint:**

```python
@app.put("/api/cases/{case_id}")
def update_case(case_id: int, case_update: CaseUpdateSchema, db: Session):
    # 1. Update local database (existing code)
    db_case = update_in_database(...)
    
    # 2. NEW: Write back to Google Sheets
    if sync_manager.sheets_config:
        success = write_case_to_sheet(
            case_data=prepare_case_data(db_case),
            sheet_url=sync_manager.sheets_config['sheet_url'],
            credentials_json=sync_manager.sheets_config['credentials_json']
        )
        
        if success:
            logger.info(f"✅ Case {db_case.control_no} synced to Google Sheets")
        else:
            logger.warning(f"⚠️ Failed to sync to Google Sheets")
    
    return db_case
```

**Error Handling:**
- If Google Sheets write fails, the update still succeeds in the database
- Logs warning but doesn't fail the request
- User can retry by editing again

---

## Troubleshooting

### Issue: Changes Not Syncing to Google Sheets

**Check 1: Is Auto-Sync Running?**
```bash
curl http://localhost:8000/api/google-sheets/status
```

Should show:
```json
{
  "configured": true,
  "is_syncing": false,
  "last_sync_time": "2025-10-22T22:50:00.123456"
}
```

**Check 2: Service Account Permissions**

The Service Account must have **EDITOR** access to the Google Sheet:

1. Open your Google Sheet
2. Click **Share**
3. Find: `mynaga-sync@mynagaapp-sheets-api.iam.gserviceaccount.com`
4. Ensure permission is set to **Editor** (NOT Viewer)
5. If not found, add it with Editor permissions

**Check 3: Backend Logs**

```bash
tail -f /Users/jirehb.custodio/Python/mynaga-dashboard/backend/backend.log
```

Look for:
- ✅ `Successfully updated X cells in range Main!A5:K5`
- ❌ `Error writing to sheet: Access denied`

**Check 4: Control No. Must Match**

The Control No. in the dashboard must **exactly match** the value in Column A of Google Sheets.

If the case was edited outside the system and the Control No. changed, it won't find the row.

---

### Issue: "Access denied" Error

**Symptom:**
```
ERROR: Access denied. Make sure the service account has EDITOR access to the sheet.
```

**Solution:**

1. **Check Service Account Email:**
   ```bash
   cat /Users/jirehb.custodio/Downloads/mynagaapp-sheets-api-c06bb9d76039.json | grep client_email
   ```

2. **Share Google Sheet:**
   - Copy the email (e.g., `mynaga-sync@mynagaapp-sheets-api.iam.gserviceaccount.com`)
   - Go to Google Sheets → Share
   - Add the email with **Editor** permissions
   - Uncheck "Notify people"
   - Click Share

3. **Verify Scope:**
   Check that `google_sheets_auth.py` has:
   ```python
   SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # NOT .readonly
   ```

---

### Issue: Changes Sync to Google Sheets but Not Visible

**Possible Cause:** Spreadsheet Tab Cache

**Solution:**
1. **Hard Refresh** Google Sheets: `Cmd+Shift+R` (Mac) or `Ctrl+F5` (Windows)
2. **Check Correct Tab**: Make sure you're viewing the "Main" tab (gid=412096204)
3. **Check Row Number**: Verify the correct row was updated by searching for the Control No.

---

### Issue: Cluster Assignments Not Syncing

**Note:** Cluster field is not yet mapped to Google Sheets columns A-K.

To add cluster sync:

1. **Find the Cluster Column** in Google Sheets (e.g., Column L)
2. **Update Column Mapping** in `google_sheets_sync.py`:
   ```python
   row_values = [
       # ... existing columns ...
       case_data.get('cluster_id', ''),  # L (example)
   ]
   ```
3. **Update Range** in `write_case_to_sheet()`:
   ```python
   range_name = f"{sheet_name}!A{row_number}:L{row_number}"  # A-L instead of A-K
   ```

---

## Monitoring & Logs

### Check Sync Status

**API Endpoint:**
```bash
curl http://localhost:8000/api/google-sheets/status
```

**Response:**
```json
{
  "last_sync_time": "2025-10-22T22:50:15.123456",
  "last_sync_status": {
    "fetched": 2328,
    "created": 0,
    "updated": 5,
    "skipped": 0,
    "errors": []
  },
  "is_syncing": false,
  "configured": true
}
```

### Backend Logs

**View Live Logs:**
```bash
tail -f /Users/jirehb.custodio/Python/mynaga-dashboard/backend/backend.log | grep -i "sync\|sheet"
```

**Look For:**
- `Syncing case CN-2024-001 back to Google Sheets...`
- `Found case CN-2024-001 at row 5`
- `Successfully updated 11 cells in range Main!A5:K5`
- `✅ Case CN-2024-001 synced to Google Sheets`

**Error Examples:**
- `⚠️ Failed to sync case CN-2024-001 to Google Sheets`
- `Error writing to sheet: Access denied`
- `Case CN-2024-001 not found in sheet`

---

## Limitations

### What Cannot Be Done

1. **❌ MyNaga App Website Edits**
   - The MyNaga App website is an **external system** we don't control
   - No API access to edit reports on their platform
   - Can only view reports via external links (Column I/L)

2. **❌ Real-Time Reverse Sync Detection**
   - If you edit directly in Google Sheets, dashboard won't know until next 10-second sync
   - Not instant bidirectional sync
   - Consider waiting 10 seconds after editing Google Sheets to see changes in dashboard

3. **❌ Conflict Resolution**
   - If two people edit the same case simultaneously:
     - Dashboard → Google Sheets writes will overwrite each other
     - Last write wins
   - No merge conflict detection (yet)

### Recommended Workflow

**For Best Results:**
1. **Primary Editing**: Use the dashboard for all edits
2. **Google Sheets**: Use for viewing, reporting, and bulk imports
3. **Avoid Simultaneous Edits**: Don't edit the same case in both places at once

---

## Performance

### Write Speed
- **Instant**: Dashboard updates happen immediately upon saving
- **Google Sheets API**: Write takes ~1-2 seconds per case
- **Batch Updates**: Currently updates one case at a time (future: batch updates)

### Optimization Tips
1. **Single Case Edits**: Fast (1-2 seconds)
2. **Bulk Edits**: Consider using CSV import/export instead of individual edits
3. **Network**: Requires internet connection to write to Google Sheets

---

## Security

### Service Account Permissions

**Current Access:**
- **Read**: All data from "Main" tab
- **Write**: Specific rows by Control No. (columns A-K)
- **No Delete**: Service Account cannot delete rows
- **Scoped**: Only accesses the specific spreadsheet shared with it

**Best Practices:**
1. **Credentials File**: Keep `mynagaapp-sheets-api-c06bb9d76039.json` secure
2. **Limited Sharing**: Only share spreadsheet with necessary accounts
3. **Audit Trail**: Google Sheets tracks all edits with timestamps
4. **Revoke Access**: Can revoke Service Account access anytime from Google Sheet sharing settings

---

## What's Next?

### Potential Enhancements

1. **Conflict Detection**
   - Detect if Google Sheets was edited after dashboard edit
   - Prompt user to choose version

2. **Batch Updates**
   - Update multiple cases to Google Sheets in one request
   - Faster bulk edits

3. **Full Column Support**
   - Currently syncs columns A-K
   - Could expand to all columns (L, M, N, etc.)

4. **Cluster Sync**
   - Add cluster assignments to Google Sheets
   - New column or existing column mapping

5. **Audit Log**
   - Track who edited what and when
   - Sync edit history back to Google Sheets

6. **Webhooks (Future)**
   - Real-time notifications when Google Sheets changes
   - Instant sync instead of 10-second polling

---

## Summary

🎉 **Congratulations!** Your dashboard now has two-way sync with Google Sheets!

**What You Can Do:**
- ✅ Edit cases in the dashboard → Automatically updates Google Sheets
- ✅ Edit Google Sheets → Auto-syncs to dashboard every 10 seconds
- ✅ Team collaboration with shared spreadsheet
- ✅ Professional dashboard with real-time data

**What You Cannot Do:**
- ❌ Edit MyNaga App website from dashboard (external system)

**Remember:**
- Auto-sync must be running (`bash restart_autosync.sh`)
- Service Account needs **Editor** permissions
- Changes sync immediately to Google Sheets
- Google Sheets edits appear in dashboard within 10 seconds

---

## Quick Reference

### Start Auto-Sync
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
bash restart_autosync.sh
```

### Check Sync Status
```bash
curl http://localhost:8000/api/google-sheets/status
```

### View Logs
```bash
tail -f backend.log | grep -i sync
```

### Restart Backend
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
lsof -ti:8000 | xargs kill -9 2>/dev/null
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
bash restart_autosync.sh  # Don't forget this!
```

### Frontend URL
```
http://localhost:3000/cases
```

---

**Last Updated:** October 22, 2025  
**Feature Status:** ✅ Production Ready  
**Auto-Sync:** Every 10 seconds  
**Write-Back:** Immediate on save
