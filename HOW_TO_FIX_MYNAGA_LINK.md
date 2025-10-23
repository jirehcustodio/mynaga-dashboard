# 🔗 MyNaga Report Links - SOLVED! ✅

## ✅ Problem Solved!

**Correct MyNaga URL Format:**
```
https://mynaga.app/reports?_id=68f8cce4fb16457f30003544
```

## Key Discovery

MyNaga uses **MongoDB `_id`** in the URL, NOT the `control_no`.

Example:
- Control No: `OTH-251022-2523`
- MongoDB ID: `68f8cce4fb16457f30003544`
- Correct URL: `https://mynaga.app/reports?_id=68f8cce4fb16457f30003544`

## Solution

**Update Column L in your Google Sheet** with the actual MyNaga report URLs.

### Before (Current State):
```
| Control No      | Link to Report |
|-----------------|----------------|
| OTH-251022-2523 | Link           |
| DRK-250818-001  | Link           |
```

### After (What You Need):
```
| Control No      | Link to Report |
|-----------------|----------------------------------------|
| OTH-251022-2523 | https://mynaga.app/reports?_id=68f8... |
| DRK-250818-001  | https://mynaga.app/reports?_id=67123...|
```

## How the Dashboard Works Now

The "View in MyNaga App" button will:
1. ✅ Only show if Column L has a real URL (starts with http)
2. ✅ Use the exact URL from your Google Sheet
3. ✅ Open the specific MyNaga report

**No URL in Column L?** → Button hidden
**URL in Column L?** → Button visible and working ✅

## How to Get MongoDB IDs

You need to get the MongoDB `_id` values from MyNaga. Options:

### Option 1: From MyNaga's URL
1. Open https://mynaga.app
2. Navigate to a report (e.g., OTH-251022-2523)
3. Look at the URL: `https://mynaga.app/reports?_id=68f8cce4fb16457f30003544`
4. Copy the `_id` value
5. Paste into Column L as full URL

### Option 2: MyNaga API/Export
Ask MyNaga team for:
- API endpoint to get report by control_no
- CSV export with both control_no and _id
- Admin panel with "Copy Link" feature

### Option 3: Bulk Update Script
If you have access to MyNaga's database/API, I can help create a script to:
1. Fetch all reports with their _id values
2. Auto-update Column L in Google Sheets

## Testing

After updating Column L:
1. Wait 10 seconds (auto-sync)
2. Click a case in dashboard
3. "View in MyNaga App" button should appear
4. Click it → Opens correct report ✅

## Why We Can't Auto-Generate

**Problem:** We don't have MongoDB IDs in the dashboard

The dashboard has:
- ✅ Control Number (e.g., `OTH-251022-2523`)
- ❌ MongoDB _id (needed for URL)

**Solutions:**
1. ✅ Update Column L with real URLs (recommended)
2. 🔄 Ask MyNaga for API to convert control_no → _id

---

**See also:** `UPDATE_MYNAGA_LINKS.md` for detailed instructions.

**Current Status:** Dashboard ready. Just need to populate Column L with actual MyNaga URLs!

### Method 1: Check MyNaga Website Directly (EASIEST)
1. Open https://mynaga.app in your browser
2. Navigate to ANY report (use the MyNaga interface)
3. Look at the URL in your browser's address bar
4. Copy the entire URL

**Examples of what you might see:**
```
✅ https://mynaga.app/#/report/DRK-250818-001
✅ https://mynaga.app/?report=DRK-250818-001
✅ https://mynaga.app/case/DRK-250818-001
✅ https://app.mynaga.ph/view?id=DRK-250818-001
```

### Method 2: Contact MyNaga Developers
Ask them: *"What's the URL format to link directly to a specific report? Example: DRK-250818-001"*

## Configure the Dashboard

Once you have the correct URL pattern, update the code:

### File: `frontend/src/components/CaseModal.jsx`
Around **line 398**, you'll see:

```jsx
// ============================================================
// CONFIGURE THIS: Update to match MyNaga's actual URL pattern
// ============================================================
// Option 1: Hash-based routing (most common for SPAs)
: `https://mynaga.app/#/report/${caseData.control_no}`
```

**Uncomment the correct option** based on what you discovered:

```jsx
// Option 1: Hash-based routing
: `https://mynaga.app/#/report/${caseData.control_no}`

// Option 2: Query parameter
// : `https://mynaga.app/?report=${caseData.control_no}`

// Option 3: Path-based routing
// : `https://mynaga.app/reports/${caseData.control_no}`

// Option 4: Case endpoint
// : `https://mynaga.app/case/${caseData.control_no}`

// Option 5: View endpoint
// : `https://mynaga.app/view?id=${caseData.control_no}`
```

### Examples

**If MyNaga uses hash routing like** `https://mynaga.app/#/report/DRK-250818-001`:
```jsx
: `https://mynaga.app/#/report/${caseData.control_no}`
```

**If MyNaga uses query params like** `https://mynaga.app/?id=DRK-250818-001`:
```jsx
: `https://mynaga.app/?id=${caseData.control_no}`
```

**If MyNaga uses different path like** `https://mynaga.app/view-report/DRK-250818-001`:
```jsx
: `https://mynaga.app/view-report/${caseData.control_no}`
```

## Test the Fix

1. Save the file
2. The frontend should auto-reload (Vite hot reload)
3. Click any case in the dashboard
4. Click "View in MyNaga App" button
5. Check browser console for log: `🔗 Opening MyNaga report: https://...`
6. Verify it opens the correct report page (not homepage)

## Advanced: Update Google Sheets (Optional)

Instead of constructing URLs, you can put the actual report URLs in **Column L**:

1. Open your Google Sheet
2. Go to **Column L** (Link to Report)
3. Replace "Link" text with actual URLs:
   ```
   https://mynaga.app/#/report/DRK-250818-001
   https://mynaga.app/#/report/DRK-250818-002
   https://mynaga.app/#/report/DRK-250818-003
   ```

The dashboard will automatically use these URLs instead of constructing them.

## Debugging

If it still doesn't work:

1. Open browser DevTools (F12)
2. Click "View in MyNaga App" button
3. Check Console tab for:
   ```
   🔗 Opening MyNaga report: https://mynaga.app/#/report/DRK-250818-001
   📋 Control No: DRK-250818-001
   ```
4. Copy the URL and test it directly in a new browser tab
5. If it redirects to homepage, the URL pattern is still wrong

## Common MyNaga URL Patterns

Based on typical SPA frameworks:

| Framework | Typical Pattern |
|-----------|----------------|
| React Router (Hash) | `/#/report/{id}` |
| React Router (Browser) | `/report/{id}` |
| Angular | `/#/report/{id}` |
| Vue Router (Hash) | `/#/report/{id}` |
| Next.js | `/report/{id}` or `/report?id={id}` |

## Need Help?

1. Share the URL you see when viewing a report in MyNaga
2. Share any error messages from browser console
3. Share a screenshot of the MyNaga report page URL

---

**Current Status:** Using `https://mynaga.app/#/report/${control_no}` as most likely pattern (hash-based routing is most common for SPAs).
