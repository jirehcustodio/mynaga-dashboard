# How to Set Up Google Sheets API Credentials

## Steps to Enable Python Script to Update Sheets

### 1. Create Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google Sheets API**
4. Go to **IAM & Admin → Service Accounts**
5. Click **Create Service Account**
6. Name it `mynaga-dashboard` 
7. Click **Create and Continue**
8. Skip roles (click Continue)
9. Click **Done**

### 2. Create JSON Key
1. Click on the service account you just created
2. Go to **Keys** tab
3. Click **Add Key → Create new key**
4. Choose **JSON**
5. Download the JSON file

### 3. Share Your Google Sheet
1. Open the downloaded JSON file
2. Find the `client_email` field (looks like `mynaga-dashboard@...iam.gserviceaccount.com`)
3. Copy this email
4. Open your Google Sheet
5. Click **Share** button
6. Paste the service account email
7. Give it **Editor** access
8. Click **Send**

### 4. Install the Credentials
```bash
# Move the downloaded JSON to backend folder
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
mv ~/Downloads/mynaga-dashboard-*.json google-credentials.json

# Set environment variable
export GOOGLE_SHEETS_CREDENTIALS="google-credentials.json"
```

### 5. Run the Script Again
```bash
python3 fetch_mynaga_ids.py 1c9OgQ_fr-Ia33wnXh3tC1JTh8hyaSoOIwME0RrAG7Uo 2025-08-01 2025-10-31
```

---

## OR Just Use AppScript! 😊

**Your AppScript already does this!** Just run it from:
- Extensions → Apps Script → Run

The Python script is useful if you want to automate it, but AppScript works perfectly for manual updates.
