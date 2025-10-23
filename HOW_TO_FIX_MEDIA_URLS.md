# 🔧 How to Fix Media URLs - Show Photos & Videos

## 🎯 The Problem

You're seeing placeholder icons instead of actual photos and videos because the system doesn't know where MyNaga app stores the media files.

**Current Status:**
- ✅ Media feature is working
- ✅ Filenames are syncing from Google Sheets
- ❌ Need to configure the correct storage URL

---

## 🔍 What You'll See

### Before Fix:
- 📎 Placeholder icons with filenames
- "Images not loading?" button appears
- Clicking shows error message with attempted URL

### After Fix:
- 🖼️ Actual photos and videos display
- Click to zoom/play works perfectly
- Professional gallery view

---

## 🛠️ How to Fix It

### Step 1: Find the Correct Storage URL

You need to find where MyNaga app stores uploaded files. Try these methods:

#### Option A: Check MyNaga App Code
Look in the MyNaga mobile app's code for where files are uploaded:

```javascript
// Look for patterns like:
- Firebase Storage initialization
- AWS S3 bucket configuration  
- File upload endpoints
- Image/video storage paths
```

#### Option B: Check Firebase Console
If MyNaga uses Firebase (most common):

1. Open Firebase Console: https://console.firebase.google.com
2. Select your MyNaga project
3. Go to **Storage** section
4. Look for a **reports** or **media** folder
5. Click on a file to see its URL structure

**Example Firebase URL:**
```
https://firebasestorage.googleapis.com/v0/b/mynaga-app.appspot.com/o/reports%2Fcompressed_Screenshot.jpg?alt=media
```

#### Option C: Check a Real Report
1. Open MyNaga mobile app or website
2. Find a report with a photo
3. Right-click the image → "Copy image address"
4. Look at the URL pattern

**Example URL patterns:**
```
https://mynaga.app/storage/reports/filename.jpg
https://api.mynaga.app/files/reports/filename.jpg
https://storage.googleapis.com/mynaga-bucket/reports/filename.jpg
```

#### Option D: Ask MyNaga Developers
Contact the MyNaga app development team and ask:
> "Where are report attachments stored? What's the base URL for accessing uploaded images?"

---

### Step 2: Update the Configuration

Once you have the correct base URL, update the code:

**File:** `frontend/src/components/CaseModal.jsx`  
**Line:** ~36

**Find this section:**
```javascript
// Current placeholder - UPDATE THIS!
const MYNAGA_STORAGE_BASE = 'https://mynaga.app/storage/reports/'
```

**Replace with your actual URL:**

#### If Using Firebase Storage:
```javascript
const MYNAGA_STORAGE_BASE = 'https://firebasestorage.googleapis.com/v0/b/mynaga-app.appspot.com/o/reports%2F'

// Note: For Firebase, you might also need to add '?alt=media' at the end
// Update the return line to:
return MYNAGA_STORAGE_BASE + encodeURIComponent(urlOrFilename) + '?alt=media'
```

#### If Using Direct Server:
```javascript
const MYNAGA_STORAGE_BASE = 'https://mynaga.app/api/storage/reports/'
// or
const MYNAGA_STORAGE_BASE = 'https://api.mynaga.app/files/'
```

#### If Using AWS S3:
```javascript
const MYNAGA_STORAGE_BASE = 'https://mynaga-reports.s3.amazonaws.com/'
// or with region:
const MYNAGA_STORAGE_BASE = 'https://mynaga-reports.s3.ap-southeast-1.amazonaws.com/'
```

#### If Using Google Cloud Storage:
```javascript
const MYNAGA_STORAGE_BASE = 'https://storage.googleapis.com/mynaga-reports/'
```

---

### Step 3: Test It

1. **Save the file** (Vite will auto-reload)
2. **Refresh your browser** at http://localhost:3000/cases
3. **Click any case** to open the detail modal
4. **Scroll to "Attached Media"** section
5. **Check if images load**

---

## 🧪 Debugging Tools

### Check Browser Console

1. Open browser (Chrome/Edge/Firefox)
2. Press **F12** to open DevTools
3. Click **Console** tab
4. Look for messages like:

**When attempting to load media:**
```
🔗 Attempting to load media: https://mynaga.app/storage/reports/compressed_Screenshot.jpg
```

**If it fails:**
```
❌ Failed to load image: https://mynaga.app/storage/reports/compressed_Screenshot.jpg
```

**Check the Network tab:**
1. Open DevTools (F12)
2. Click **Network** tab
3. Filter by **Img** or **Media**
4. Click on a case to trigger media loading
5. See if requests are failing (red color)
6. Click failed request to see error details

### Common Errors and Fixes

#### Error: 404 Not Found
**Meaning:** File doesn't exist at that URL  
**Fix:** Base URL is wrong or file path structure is different

#### Error: 403 Forbidden
**Meaning:** Access denied  
**Fix:** Files need public read permissions or authentication

#### Error: CORS Policy Error
**Meaning:** Server blocking cross-origin requests  
**Fix:** Storage bucket needs CORS configuration (Firebase/S3)

**Firebase CORS Fix:**
```bash
# Create cors.json:
[
  {
    "origin": ["*"],
    "method": ["GET"],
    "maxAgeSeconds": 3600
  }
]

# Apply:
gsutil cors set cors.json gs://your-bucket-name
```

---

## 📋 Sample Configurations

### Configuration 1: Firebase Storage (Most Common)

**File:** `CaseModal.jsx` (Line ~36)

```javascript
const getMediaUrl = (urlOrFilename) => {
  if (urlOrFilename.startsWith('http://') || urlOrFilename.startsWith('https://')) {
    return urlOrFilename
  }
  
  // Firebase Storage configuration
  const FIREBASE_PROJECT = 'mynaga-app' // Your Firebase project ID
  const STORAGE_BUCKET = `${FIREBASE_PROJECT}.appspot.com`
  const FOLDER_PATH = 'reports'
  
  const MYNAGA_STORAGE_BASE = `https://firebasestorage.googleapis.com/v0/b/${STORAGE_BUCKET}/o/${FOLDER_PATH}%2F`
  
  // Firebase requires URL encoding and ?alt=media for direct access
  return MYNAGA_STORAGE_BASE + encodeURIComponent(urlOrFilename) + '?alt=media'
}
```

### Configuration 2: Direct Server

```javascript
const getMediaUrl = (urlOrFilename) => {
  if (urlOrFilename.startsWith('http://') || urlOrFilename.startsWith('https://')) {
    return urlOrFilename
  }
  
  const MYNAGA_STORAGE_BASE = 'https://mynaga.app/storage/reports/'
  return MYNAGA_STORAGE_BASE + urlOrFilename
}
```

### Configuration 3: AWS S3

```javascript
const getMediaUrl = (urlOrFilename) => {
  if (urlOrFilename.startsWith('http://') || urlOrFilename.startsWith('https://')) {
    return urlOrFilename
  }
  
  const S3_BUCKET = 'mynaga-reports'
  const S3_REGION = 'ap-southeast-1' // Your AWS region
  const FOLDER_PATH = 'reports'
  
  const MYNAGA_STORAGE_BASE = `https://${S3_BUCKET}.s3.${S3_REGION}.amazonaws.com/${FOLDER_PATH}/`
  return MYNAGA_STORAGE_BASE + urlOrFilename
}
```

---

## ✅ Verification Checklist

After updating the URL, verify:

- [ ] Images load in the gallery thumbnails
- [ ] Clicking a thumbnail opens full-screen view
- [ ] Videos play with controls
- [ ] No 404 errors in browser console
- [ ] No CORS errors in browser console
- [ ] "Images not loading?" button doesn't appear
- [ ] Multiple images per case display correctly

---

## 🎬 Example: Testing with Real Data

### Your Current Data:
You have **2,329 cases** with media filenames like:
- `compressed_Screenshot_20250818-142557_Messenger.jpg`
- `compressed_5e00025e3491e97e144e2da031cc54e2_exif.jpg`
- `compressed_5aa810380ac6e2699f869894858eca39_exif.jpg`

### Test Cases:
1. **DRK-250818-001**: Should show a screenshot from Messenger
2. **WLK-250818-002**: Should show an EXIF image
3. **PTR-250818-003**: Should show another photo

### Testing Steps:
1. Open dashboard: http://localhost:3000/cases
2. Search for "DRK-250818-001"
3. Click the case
4. Scroll to "Attached Media"
5. If you see the actual photo → ✅ Success!
6. If you see placeholder → Check console for attempted URL

---

## 🆘 Still Not Working?

### Quick Checklist:

1. **Is the frontend running?**
   ```bash
   lsof -i:3000
   ```

2. **Did you save the file?**
   - Vite should auto-reload
   - Check browser console for reload message

3. **Is the URL correct?**
   - Copy the attempted URL from console
   - Paste it directly in browser
   - See if it loads the image

4. **Are the files actually there?**
   - Files might have been deleted
   - Files might be in a different folder
   - Filenames might have changed

5. **Do you have permissions?**
   - Storage bucket might require authentication
   - Files might not be publicly accessible

---

## 📞 Getting Help

### Information to Gather:

When asking for help, provide:

1. **What you see:** Screenshot of the placeholder view
2. **Browser console output:** Copy error messages
3. **Attempted URL:** From console log (🔗 Attempting to load...)
4. **MyNaga app type:** Web, mobile, hybrid?
5. **Hosting provider:** Firebase, AWS, own server?

### Where to Ask:

- MyNaga app development team
- Your Firebase/AWS administrator
- System administrator who deployed MyNaga

---

## 💡 Pro Tips

### Tip 1: Test with One Case First
Don't try to fix all cases at once. Find one case with media, get that working, then all others will work.

### Tip 2: Use Browser DevTools
The Network tab shows exactly what's happening with each request. This is your best debugging tool.

### Tip 3: Check Public Access
If using Firebase/S3, make sure files have public read permissions. Private files need authentication tokens.

### Tip 4: Look at MyNaga App Website
If MyNaga has a web version, open a report there and inspect the image URLs using DevTools.

---

## 🎉 Once It's Working

After fixing the URL, you'll have:

- ✨ Full photo gallery for every report
- ✨ Click-to-zoom on images
- ✨ Video playback with controls
- ✨ Professional, government-style presentation
- ✨ Automatic sync every 10 seconds

**You'll be able to:**
- Verify citizen reports visually
- See the actual problems reported
- Review multiple photos per case
- Play video evidence directly
- Make better decisions with visual context

---

## 📚 Related Documentation

- **MEDIA_QUICKSTART.md** - Quick start guide for media feature
- **ATTACHED_MEDIA_FEATURE.md** - Complete feature documentation
- **DOCUMENTATION_INDEX.md** - All documentation overview

---

**Current Status:** ⚠️ Configuration Needed  
**Next Step:** Find and update the storage base URL  
**Time Needed:** 10-15 minutes once you have the correct URL

Good luck! 🚀
