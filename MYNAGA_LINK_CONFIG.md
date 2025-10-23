# 🔗 MyNaga Link Configuration - Complete Guide

## Problem
The "View in MyNaga App" button needs MongoDB `_id` values to create correct URLs.

**Correct URL format:**
```
https://mynaga.app/reports?_id=68f8cce4fb16457f30003544
```

## ⚡ Quick Solution

**You have a MyNaga Bearer token!** Let me help you use it.

### What We Need to Know:

1. **What's the correct MyNaga API endpoint?**
   - Ask MyNaga team: "What's the API endpoint to fetch all reports?"
   - Common patterns: `/api/reports`, `/api/v1/reports`, etc.

2. **Is your token still valid?**
   - JWT tokens expire (yours expires: 1761186348 = ~Feb 2026)
   - If API returns 401, get a fresh token

### Three Ways to Update Column L

---

## Option 1: Automatic API Fetch (Best!)

**If MyNaga API is working:**

```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend

# Test the API first
python3 test_mynaga_api.py

# If successful, run the full import
python3 fetch_mynaga_ids.py
```

**What it does:**
- ✅ Fetches all reports from MyNaga
- ✅ Extracts control_no → _id mappings  
- ✅ Updates Column L in Google Sheets
- ✅ All 2,329 cases updated automatically!

---

## Option 2: Manual CSV Import

**If you can export data from MyNaga:**

1. Export CSV with these columns:
   ```
   control_no,_id
   OTH-251022-2523,68f8cce4fb16457f30003544
   DRK-250818-001,67123abc45def67890123456
   ```

2. Save as `mynaga_ids.csv` in backend folder

3. Run:
   ```bash
   python3 import_mynaga_urls.py
   ```

---

## Option 3: Manual Copy-Paste

For small datasets:

1. Open MyNaga, navigate to report
2. Copy URL: `https://mynaga.app/reports?_id=68f8cce4fb16457f30003544`
3. Paste into Column L of Google Sheet
4. Wait 10 seconds for auto-sync

---

## How It Works Now

**Button only appears if Column L has real URL:**

```jsx
// frontend/src/components/CaseModal.jsx
{caseData.link_to_report && 
 caseData.link_to_report !== 'Link' && 
 caseData.link_to_report.startsWith('http') && (
  <a href={caseData.link_to_report}>View in MyNaga App</a>
)}
```

**Status:**
- ❌ Column L = "Link" → Button hidden
- ✅ Column L = `https://mynaga.app/reports?_id=...` → Button works!

---

## Test One Case First

**Quick test with OTH-251022-2523:**

1. Update Column L in Google Sheet:
   ```
   https://mynaga.app/reports?_id=68f8cce4fb16457f30003544
   ```

2. Wait 10 seconds

3. Click case in dashboard

4. "View in MyNaga App" button should appear

5. Click → Opens correct report ✅

---

## Troubleshooting

### API not working?

**Get correct endpoint from MyNaga team:**
```
Hey MyNaga team,

I need to fetch all reports via API. What's the correct endpoint?

I have a Bearer token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Thanks!
```

### Button not appearing?

**Check database:**
```bash
sqlite3 test.db "SELECT control_no, link_to_report FROM cases LIMIT 5"
```

Should show URLs, not "Link" text.

**Force sync:**
```bash
bash manual_sync.sh
```

---

## Files Created

✅ `fetch_mynaga_ids.py` - Automatic API fetcher  
✅ `import_mynaga_urls.py` - CSV importer  
✅ `test_mynaga_api.py` - API endpoint tester  
✅ `mynaga_ids_template.csv` - CSV template

---

## Next Steps

**Try Option 1 first:**
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
python3 test_mynaga_api.py
```

Share the output with me, and I'll help you complete the setup! 🚀
