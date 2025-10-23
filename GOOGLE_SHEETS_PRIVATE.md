# Google Sheets Integration - Private Data Guide

## ✅ **YES, You Can Use Private Google Sheets!**

You have **TWO options** for syncing data from Google Sheets:

---

## **Option 1: Simple CSV URL (No Authentication Required)**

### When to Use:
- Quick setup (2 minutes)
- Don't mind making sheet "public" (anyone with link can view)
- Perfect for testing

### Steps:
1. Open your Google Sheet
2. Go to **File** → **Share** → **Publish to web**
3. Select:
   - **Sheet**: Choose your sheet (e.g., "Sheet1")
   - **Format**: Choose "Comma-separated values (.csv)"
4. Click **"Publish"**
5. Copy the published CSV URL
6. Paste it in the dashboard at **http://localhost:3000/google-sheets**

### ⚠️ Important:
- Sheet will be publicly accessible via the CSV URL
- Anyone with the URL can view the data
- Good for non-sensitive or already-public data

---

## **Option 2: Private Sheet with Service Account (SECURE - Recommended for Private Data!)**

### When to Use:
- Your data is sensitive/confidential
- Sheet must remain private
- Professional/production environment
- You want full control over access

### Steps:

#### 1. Create Google Cloud Service Account (One-time setup - 10 minutes)

1. **Go to Google Cloud Console**: https://console.cloud.google.com

2. **Create Project:**
   - Click "Select a project" → "New Project"
   - Name: "MyNaga Dashboard"
   - Click "Create"

3. **Enable Google Sheets API:**
   - In search bar, type "Google Sheets API"
   - Click "Google Sheets API" 
   - Click "ENABLE"

4. **Create Service Account:**
   - Left menu → "IAM & Admin" → "Service Accounts"
   - Click "**+ CREATE SERVICE ACCOUNT**"
   - **Service account name**: `mynaga-sync`
   - **Service account ID**: (auto-filled)
   - Click "CREATE AND CONTINUE"
   - Skip role selection → Click "CONTINUE"
   - Click "DONE"

5. **Generate Credentials JSON:**
   - Click on the service account you just created
   - Go to "**KEYS**" tab
   - Click "ADD KEY" → "Create new key"
   - Choose "**JSON**"
   - Click "CREATE"
   - **A JSON file will download** → **Save it securely!**

#### 2. Share Your Private Sheet with Service Account

1. **Open your Google Sheet** (keep it private!)

2. **Find Service Account Email:**
   - Open the downloaded JSON file
   - Find the email (looks like): `mynaga-sync@project-name.iam.gserviceaccount.com`
   - Copy this email

3. **Share the Sheet:**
   - In your Google Sheet, click "**Share**" button (top right)
   - Paste the service account email in "Add people and groups"
   - Set permission: **"Viewer"**
   - **IMPORTANT:** Uncheck "**Notify people**" (service accounts can't receive emails)
   - Click "**Share**"

#### 3. Upload Credentials to Dashboard

1. **Go to**: http://localhost:3000/google-sheets

2. **Upload the JSON file** OR **paste JSON content** in the credentials field

3. **Enter your Google Sheets URL** (the regular URL, like):
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
   ```

4. Click "**Test Connection**" to verify

5. Click "**Sync Now**"

---

## **Which Option Should You Choose?**

| Feature | Option 1: CSV URL | Option 2: Service Account |
|---------|------------------|---------------------------|
| **Setup Time** | 2 minutes | 10 minutes (one-time) |
| **Security** | Public with link | Fully private |
| **Best For** | Testing, public data | Production, sensitive data |
| **Google Sheet** | Must publish to web | Stays completely private |
| **Authentication** | None required | Service account JSON |
| **Access Control** | Anyone with URL | Only service account |

---

## **Need Help?**

### I want quick testing → Use **Option 1**
### I have private/sensitive data → Use **Option 2**

---

## **FAQ**

### Q: Can I use Option 2 with my existing private sheet?
**A:** Yes! Your sheet stays private. Just share it with the service account email.

### Q: Where do I put the JSON file?
**A:** You can either:
1. Upload it via the dashboard (http://localhost:3000/google-sheets)
2. Store it securely on the server and configure the path

### Q: Is my data safe with Option 2?
**A:** Yes! Only your service account has access. The sheet remains private to your Google account.

### Q: Can I switch from Option 1 to Option 2 later?
**A:** Absolutely! Just unpublish the CSV and set up service account authentication.

### Q: What's the difference in the URL?
**A:**
- **Option 1**: Uses CSV export URL (https://docs.google.com/spreadsheets/d/ID/export?format=csv)
- **Option 2**: Uses regular sheet URL (https://docs.google.com/spreadsheets/d/ID/edit)

---

## **Quick Start for Private Data (TL;DR)**

```bash
# Option 2 - Full Privacy
1. Create Google Cloud Project → Enable Sheets API
2. Create Service Account → Download JSON key
3. Share your private Google Sheet with: service-account@project.iam.gserviceaccount.com
4. Upload JSON in dashboard
5. Enter sheet URL
6. Test → Sync!
```

**Your private data stays private! 🔒**
