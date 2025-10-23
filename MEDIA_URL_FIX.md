# 🎯 QUICK FIX: Find MyNaga Storage URL

## The Issue
Images show **"Media Not Available"** because we need the correct storage URL.

**Attempted URL (not working):**
```
https://mynaga.app/storage/reports/compressed_IMG_20251022_180642.jpg
```

---

## ✅ Solution: 3 Steps to Fix

### Step 1: Find the Real URL (Choose ONE method)

#### Method A: Ask MyNaga Developers ⭐ EASIEST
**Contact the MyNaga app development team and ask:**

> "Hi! I'm integrating with the MyNaga dashboard. Where are citizen report attachments (photos/videos) stored? What's the base URL to access them?"
> 
> Example: `compressed_IMG_20251022_180642.jpg`

**They should give you something like:**
- `https://firebasestorage.googleapis.com/v0/b/[bucket-name]/o/...`
- `https://mynaga.app/api/media/...`
- `https://storage.googleapis.com/mynaga-bucket/...`

#### Method B: Check MyNaga Website
1. Go to https://mynaga.app
2. Open a case/report that has a photo
3. **Right-click the photo** → "Inspect" (or F12)
4. Look at the `<img src="...">` tag
5. Copy the full URL

**Example:**
```html
<img src="https://firebasestorage.googleapis.com/v0/b/mynaga123/o/reports%2Fphoto.jpg?alt=media">
```

The base URL is: `https://firebasestorage.googleapis.com/v0/b/mynaga123/o/reports%2F`

#### Method C: Check Firebase Console (if you have access)
1. Go to https://console.firebase.google.com
2. Select **MyNaga project**
3. Click **Storage** in left sidebar
4. Look for uploaded files
5. Click a file to see its URL

---

### Step 2: Update the Code

**File:** `frontend/src/components/CaseModal.jsx`  
**Line:** ~25-40

**Find this section:**
```javascript
// Current placeholder (will show filenames but not load images)
const MYNAGA_STORAGE_BASE = 'https://mynaga.app/storage/reports/'
```

**Replace based on what you found:**

#### If Firebase Storage:
```javascript
// Comment out the placeholder
// const MYNAGA_STORAGE_BASE = 'https://mynaga.app/storage/reports/'

// Uncomment and update these lines:
const FIREBASE_BUCKET = 'YOUR-BUCKET-NAME.appspot.com'  // e.g., mynaga123.appspot.com
const MYNAGA_STORAGE_BASE = `https://firebasestorage.googleapis.com/v0/b/${FIREBASE_BUCKET}/o/`
return MYNAGA_STORAGE_BASE + encodeURIComponent(urlOrFilename) + '?alt=media'
```

#### If Direct Server:
```javascript
// Replace with:
const MYNAGA_STORAGE_BASE = 'https://mynaga.app/api/media/'  // or whatever path you found
return MYNAGA_STORAGE_BASE + urlOrFilename
```

#### If AWS S3/Google Cloud:
```javascript
// Replace with:
const MYNAGA_STORAGE_BASE = 'https://your-bucket.s3.amazonaws.com/reports/'
return MYNAGA_STORAGE_BASE + urlOrFilename
```

---

### Step 3: Test

1. **Save the file** (Vite will auto-reload)
2. **Refresh browser** at http://localhost:3000/cases
3. **Click any case** (try one with recent date like 10/22/2025)
4. **Scroll to "Attached Media"**
5. **Check if images load** ✅

---

## 📞 What to Tell MyNaga Developers

If you contact the MyNaga team, send them this:

```
Hi MyNaga Team,

I'm building an integration with the Naga Dashboard to display 
citizen report attachments (photos/videos).

I have the filenames from Google Sheets (e.g., 
"compressed_IMG_20251022_180642.jpg"), but I need the base URL 
to construct the full path.

Could you provide:
1. The storage service you use (Firebase, AWS S3, etc.)
2. The base URL format to access attachments
3. Any authentication requirements

Example filename: compressed_IMG_20251022_180642.jpg

Thanks!
```

---

**Next Step:** Contact MyNaga developers or inspect the MyNaga website to find the storage URL!

Once configured, you'll have a beautiful photo/video gallery for all citizen reports! 🎉
