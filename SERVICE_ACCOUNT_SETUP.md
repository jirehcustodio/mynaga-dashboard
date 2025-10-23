# 🔐 Google Sheets Service Account Setup Guide
## Keep Your Data 100% Private

This guide will walk you through setting up **fully private** Google Sheets access using a Service Account.

---

## ⏱️ **Time Required:** 10-15 minutes (one-time setup)

## 🎯 **What You'll Get:**
- ✅ Your Google Sheet stays **completely private**
- ✅ No "Publish to web" required
- ✅ Only your application can access the data
- ✅ Enterprise-grade security

---

## 📋 **Step-by-Step Instructions**

### **Step 1: Create Google Cloud Project** (3 minutes)

1. Go to **Google Cloud Console**: https://console.cloud.google.com

2. Click the **project dropdown** (top left, next to "Google Cloud")

3. Click **"NEW PROJECT"**

4. Enter project details:
   - **Project name**: `MyNaga Dashboard` (or any name you like)
   - **Organization**: Leave as-is (No organization)
   - Click **"CREATE"**

5. Wait for project creation (~10 seconds)

6. **Select your new project** from the dropdown

---

### **Step 2: Enable Google Sheets API** (1 minute)

1. In the search bar at the top, type: **`Google Sheets API`**

2. Click on **"Google Sheets API"** in the results

3. Click the blue **"ENABLE"** button

4. Wait for it to enable (~5 seconds)

---

### **Step 3: Create Service Account** (3 minutes)

1. In the left sidebar, click **"IAM & Admin"** → **"Service Accounts"**
   - Or search for "Service Accounts" in the top search bar

2. Click **"+ CREATE SERVICE ACCOUNT"** (blue button at top)

3. **Service account details:**
   - **Service account name**: `mynaga-sync`
   - **Service account ID**: (auto-filled as `mynaga-sync`)
   - **Description**: `Service account for MyNaga dashboard Google Sheets sync`
   - Click **"CREATE AND CONTINUE"**

4. **Grant access** (Optional - Skip this):
   - Click **"CONTINUE"** (don't select any role)

5. **Grant users access** (Optional - Skip this):
   - Click **"DONE"**

---

### **Step 4: Generate JSON Key File** (2 minutes) ⚠️ IMPORTANT

1. You'll see your service account in the list. Click on it.

2. Go to the **"KEYS"** tab (at the top)

3. Click **"ADD KEY"** → **"Create new key"**

4. Choose **"JSON"** format

5. Click **"CREATE"**

6. **A JSON file will download automatically** 
   - ⚠️ **SAVE THIS FILE SECURELY!**
   - It contains your private credentials
   - You'll need it in the next steps

---

### **Step 5: Find Your Service Account Email** (30 seconds)

1. Open the downloaded JSON file with any text editor

2. Find the line that says `"client_email":`
   ```json
   "client_email": "mynaga-sync@your-project-123456.iam.gserviceaccount.com"
   ```

3. **Copy this email address** (you'll need it in the next step)

---

### **Step 6: Share Your Private Sheet** (1 minute)

1. **Open your Google Sheet** (the one with your case data)

2. Click the **"Share"** button (top right corner)

3. In the "Add people and groups" field:
   - **Paste the service account email** you copied in Step 5
   - Example: `mynaga-sync@your-project-123456.iam.gserviceaccount.com`

4. Set permission to **"Viewer"**

5. **IMPORTANT:** Uncheck **"Notify people"** 
   - (Service accounts can't receive emails)

6. Click **"Share"**

✅ **Done!** Your sheet is now accessible only to this service account.

---

### **Step 7: Configure Dashboard** (2 minutes)

1. Open your browser to: **http://localhost:3000**

2. Click **"Google Sheets"** in the left sidebar (☁️ icon)

3. Select **"Service Account (Private)"** authentication method

4. Click **"Choose File"** and upload the JSON key file you downloaded in Step 4

5. Enter your **Google Sheet URL** (the regular URL, like):
   ```
   https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit
   ```

6. Click **"Test Connection"**
   - You should see: "Successfully connected to Google Sheets via Service Account (Private)"

7. Click **"Sync Now"** to import your data

---

## ✅ **Verification**

After Step 7, you should see:
- ✅ "Connection Successful!"
- ✅ Authentication: Service Account (Private)
- ✅ Number of rows found
- ✅ List of columns

---

## 🔒 **Security Notes**

### ✅ **What's Private:**
- Your Google Sheet is **NOT public**
- Only your service account can access it
- The JSON key is stored in your browser session only
- No one else can access your sheet without the JSON key

### ⚠️ **Protect Your JSON Key:**
- **DON'T** share the JSON file with anyone
- **DON'T** commit it to Git/GitHub
- **DON'T** post it online
- **DO** keep it in a secure location
- **DO** treat it like a password

---

## 🆚 **Comparison: Service Account vs CSV Publish**

| Feature | Service Account 🔐 | CSV Publish 📄 |
|---------|-------------------|----------------|
| **Sheet Privacy** | Fully private | Accessible via URL |
| **Setup Time** | 10-15 minutes | 2 minutes |
| **Security Level** | High (Enterprise) | Medium (Unlisted) |
| **Best For** | Sensitive data | Testing, internal data |
| **Sheet URL** | Regular /edit URL | Published CSV URL |
| **Who Can Access** | Only service account | Anyone with CSV URL |

---

## 🐛 **Troubleshooting**

### Error: "Access denied" or "Permission denied"

**Solution:**
1. Make sure you shared the sheet with the **exact** service account email
2. Check that permission is set to "Viewer" (or "Editor")
3. Wait 1-2 minutes for permissions to propagate
4. Try the "Test Connection" button again

---

### Error: "Invalid credentials" or "Credentials failed"

**Solution:**
1. Make sure you uploaded the correct JSON file
2. The JSON file should be from the same project where you enabled Sheets API
3. Re-download the JSON key and try again

---

### Error: "Spreadsheet not found"

**Solution:**
1. Double-check the Google Sheets URL
2. Make sure you copied the full URL (including `https://`)
3. The URL should look like: `https://docs.google.com/spreadsheets/d/.../edit`

---

### Can't find "Service Accounts" in Google Cloud

**Solution:**
1. Make sure you're in the correct project (check top-left dropdown)
2. Try searching "Service Accounts" in the search bar at the top
3. Or navigate: **IAM & Admin** → **Service Accounts**

---

## 🎉 **You're Done!**

Your private Google Sheet is now syncing with the dashboard!

**Next steps:**
- Test the sync by adding a new row to your sheet
- Click "Sync Now" in the dashboard to update
- Check the Cases page to see your data

---

## 📚 **Additional Resources**

- **Google Cloud Console**: https://console.cloud.google.com
- **Google Sheets API Documentation**: https://developers.google.com/sheets/api
- **Service Accounts Overview**: https://cloud.google.com/iam/docs/service-accounts

---

## 🔄 **Need to Start Over?**

If something went wrong:
1. Delete the service account from Google Cloud Console
2. Create a new one following Steps 3-7
3. Generate a new JSON key
4. Re-share your sheet with the new service account email

---

## 💡 **Pro Tips**

1. **Multiple Sheets**: You can share multiple Google Sheets with the same service account email

2. **Revoke Access**: To revoke access, just remove the service account email from your sheet's sharing settings

3. **Backup Your Key**: Save the JSON key in a password manager for safekeeping

4. **Rename Service Account**: You can rename the service account anytime in Google Cloud Console

5. **Monitor Usage**: Check Google Cloud Console → IAM & Admin → Service Accounts to see API usage

---

**Questions? Need help?** Check the troubleshooting section or refer to the main documentation.

**Your data is now secure and syncing! 🎊**
