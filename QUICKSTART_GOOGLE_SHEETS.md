# 🚀 Quick Start: Google Sheets Sync (Simple Method)

## ⚡ **For Private Data - Use This Simple Method**

Your sheet can stay **unlisted** (not searchable), you just need to make it accessible via a publish link.

---

## **Step-by-Step Instructions:**

### 1. Open Your Google Sheet
Open the Google Sheet that contains your case data.

### 2. Publish Your Sheet as CSV

1. Click **File** → **Share** → **Publish to web**

2. In the dialog that appears:
   - **First dropdown**: Select the specific sheet tab (e.g., "Sheet1") or "Entire Document"
   - **Second dropdown**: Select **"Comma-separated values (.csv)"**

3. Click **"Publish"**

4. Click **"OK"** when it warns you about publishing

5. **Copy the URL** that appears (it will look like):
   ```
   https://docs.google.com/spreadsheets/d/e/XXXXX/pub?output=csv
   ```

### 3. Use in Dashboard

1. Open your browser to: **http://localhost:3000**

2. Click **"Google Sheets"** in the left sidebar (☁️ icon)

3. **Paste the CSV URL** you copied in Step 2

4. Click **"Test Connection"** to verify it works

5. Click **"Sync Now"** to import the data

---

## **Important Notes:**

### ✅ This Method:
- Your sheet is **NOT publicly searchable** on Google
- Only people with the exact URL can access it
- Perfect for internal/private data that doesn't need high security
- Takes 2 minutes to set up

### ❌ Don't Use Regular Sheet URL:
- ❌ NOT THIS: `https://docs.google.com/spreadsheets/d/YOUR_ID/edit`
- ✅ USE THIS: `https://docs.google.com/spreadsheets/d/e/YOUR_ID/pub?output=csv`

### 🔒 Need Higher Security?
If your data is highly sensitive and you don't want ANY publish link:
- See `GOOGLE_SHEETS_PRIVATE.md` for Service Account method
- Requires Google Cloud setup (10 minutes one-time)
- Sheet stays 100% private with no publish link

---

## **Expected Column Names:**

Your Google Sheet should have columns like:

| Column Name | Also Accepts | Required? |
|-------------|-------------|-----------|
| Control No. | Control No, ID, Case ID | ✅ Yes |
| Category | Type, Issue Type | No |
| Sender's Location | Location, Address | No |
| Barangay | Brgy | No |
| Description | Details | No |
| Date Created | Date, Created At | No |
| Reported by | Reporter, Name | No |
| Contact Number | Contact, Phone | No |
| Link to Report | Link, URL | No |
| MyNaga App Status | App Status | No |
| Status | Case Status | No |

**Note:** The system is flexible - it will match similar column names automatically.

---

## **Troubleshooting:**

### Error: "Connection failed" or "500 error"
**Solution:**
1. Make sure you published as **CSV** (not Web page)
2. Use the published CSV URL, not the regular sheet URL
3. Make sure your sheet has data with at least "Control No." column

### Error: "Access denied"
**Solution:**
- The publish link might not be active yet
- Try Step 2 again and make sure you clicked "Publish"
- Wait 1 minute and try again

### Data not syncing correctly
**Solution:**
1. Check your column names match the expected names above
2. Make sure "Control No." column exists and has unique values
3. Look at the sync results for specific error messages

---

## **Quick Test:**

Want to test first? Create a simple Google Sheet with:

| Control No. | Category | Description | Status |
|-------------|----------|-------------|---------|
| TEST-001 | Pothole | Road damage on Main St | OPEN |
| TEST-002 | Streetlight | Broken light on 5th Ave | RESOLVED |

Then follow steps 2-3 above!

---

## **Security Levels Comparison:**

| Method | Privacy Level | Setup Time | Who Can Access |
|--------|---------------|------------|----------------|
| **CSV Publish (This Guide)** | Medium | 2 min | Anyone with URL |
| **Service Account** | High | 10 min | Only your app |
| **No Publishing** | Private | - | Not accessible by dashboard |

---

## **Ready? Let's Go!** 🎉

1. **File** → **Share** → **Publish to web** → **CSV** → **Publish**
2. **Copy URL**
3. **Paste in dashboard** at http://localhost:3000/google-sheets
4. **Test** → **Sync** → **Done!**

Your private data is now syncing! 🔄
