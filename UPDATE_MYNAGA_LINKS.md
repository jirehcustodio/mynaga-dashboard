# 🔗 Update MyNaga Report Links in Google Sheets

## Problem Solved! ✅

The correct MyNaga URL format is:
```
https://mynaga.app/reports?_id=68f8cce4fb16457f30003544
```

**Key Finding:** MyNaga uses MongoDB `_id` (not `control_no`) in the URL.

Example:
- ❌ **Wrong:** `https://mynaga.app/reports/OTH-251022-2523`
- ✅ **Correct:** `https://mynaga.app/reports?_id=68f8cce4fb16457f30003544`

## Solution: Update Column L in Google Sheets

### Step 1: Get the MongoDB IDs from MyNaga

You need to get the actual MongoDB `_id` for each report from MyNaga. These look like:
```
68f8cce4fb16457f30003544
67123abc45def67890123456
```

### Step 2: Update Your Google Sheet

1. Open your MyNaga Status Dashboard Google Sheet
2. Go to **Column L** (Link to Report)
3. Replace "Link" text with the actual URLs:

**Example:**
| Control No | Link to Report |
|------------|----------------|
| OTH-251022-2523 | `https://mynaga.app/reports?_id=68f8cce4fb16457f30003544` |
| DRK-250818-001 | `https://mynaga.app/reports?_id=67123abc45def67890123456` |
| MAG-250920-002 | `https://mynaga.app/reports?_id=67234def56abc78901234567` |

### Step 3: Sync the Data

The dashboard auto-syncs every 10 seconds, so your changes will appear automatically!

Or manually trigger sync:
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
bash manual_sync.sh
```

## How the Button Works Now

The "View in MyNaga App" button will:
1. ✅ **Show ONLY if Column L has a real URL** (not "Link" text)
2. ✅ **Use the exact URL from the spreadsheet**
3. ✅ **Open the specific MyNaga report page**

**Before updating Column L:**
- Button hidden (because Column L has "Link" text)

**After updating Column L:**
- Button visible ✅
- Clicks open correct MyNaga report ✅

## Where to Get the MongoDB IDs?

### Option 1: Export from MyNaga Admin Panel
If MyNaga has an admin panel or API, export:
- Control Number
- MongoDB _id

### Option 2: MyNaga API
Ask MyNaga developers for an API endpoint like:
```bash
GET /api/reports?control_no=OTH-251022-2523
Response: { "_id": "68f8cce4fb16457f30003544", ... }
```

### Option 3: Manual Copy (Small Dataset)
1. Open MyNaga app
2. Navigate to each report
3. Copy the `_id` from the URL
4. Paste into Column L with format: `https://mynaga.app/reports?_id={_id}`

### Option 4: Browser Console Script (if you can access MyNaga's data)
```javascript
// Run this in MyNaga's browser console
const reports = []; // Get reports array from MyNaga
reports.forEach(r => {
  console.log(`${r.control_no}\thttps://mynaga.app/reports?_id=${r._id}`)
})
// Copy output to spreadsheet
```

## Testing

After updating a few rows in Column L:

1. Wait 10 seconds for auto-sync
2. Click a case in the dashboard
3. The "View in MyNaga App" button should now appear
4. Click it → Should open the correct MyNaga report page ✅

## Debugging

If button doesn't appear, check browser console (F12):
```
🔗 Opening MyNaga report: https://mynaga.app/reports?_id=...
📋 Control No: OTH-251022-2523
📄 Link from DB: https://mynaga.app/reports?_id=68f8cce4fb16457f30003544
```

If you see `📄 Link from DB: Link`, the URL hasn't synced yet from Google Sheets.

## Why We Can't Auto-Generate the URLs

**Problem:** The URLs require MongoDB `_id`, which we don't have in the dashboard.

**Your options:**
1. ✅ **Best:** Update Column L with actual URLs (recommended)
2. ❌ **Won't work:** Construct URLs from control_no (MyNaga doesn't support this)
3. 🔄 **Alternative:** Ask MyNaga to add an API endpoint to convert control_no → _id

## Summary

- ✅ **URL Format:** `https://mynaga.app/reports?_id={mongo_id}`
- ✅ **Update:** Put these URLs in Column L of your Google Sheet
- ✅ **Button:** Will automatically show when URL is present
- ⚠️ **Note:** Cannot construct URLs without MongoDB IDs from MyNaga

---

**Need Help?**
Share how you access MyNaga's data (API, admin panel, database) and I can help automate fetching the MongoDB IDs!
