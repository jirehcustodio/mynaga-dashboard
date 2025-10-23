# 🔧 MyNaga Real-Time Sync - Troubleshooting Guide

## ✅ Your Setup Status

**Question:** Should I push to GitHub for the auth token to work?

**Answer:** **NO!** Real-time sync works perfectly on localhost. You don't need to deploy anywhere.

---

## 🐛 Common Issue: SSL Certificate Error on macOS

### **Problem:**
```
SSL: CERTIFICATE_VERIFY_FAILED
certificate verify failed: unable to get local issuer certificate
```

### **Solution (COMPLETED ✅):**
We've already fixed this by:
1. Installing SSL certificates for Python
2. Updated the MyNaga sync client to handle SSL properly

---

## 🚀 How to Start Your Dashboard

### **Step 1: Start Backend**
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
python3 -m uvicorn main:app --reload --app-dir /Users/jirehb.custodio/Python/mynaga-dashboard/backend
```

Wait for: `Application startup complete`

### **Step 2: Start Frontend (New Terminal)**
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/frontend
npm run dev
```

Wait for: `Local: http://localhost:3000/`

### **Step 3: Open Browser**
Visit: http://localhost:3000

---

## 🔐 Configure Real-Time Sync

### **Your Token:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OGE0ODk3Zjg1ZmIxYTdiYjU2YTNjYTQiLCJpYXQiOjE3NjA1ODE1NDgsImV4cCI6MTc2MTE4NjM0OH0.AlIem843s3R_SaGLQVMjP3EfYaVMrOKANoVYv7zX3ns
```

### **Configuration Steps:**
1. Open http://localhost:3000
2. Click "MyNaga Sync" (⚡) in sidebar
3. Paste token (WITHOUT "Bearer")
4. Click "Test Connection"
5. Click "Configure"
6. Done! ✅

---

##  Why It Works on Localhost

### **Real-Time Sync Architecture:**
```
Your Browser (localhost:3000)
    ↓
Your Backend (localhost:8000)
    ↓
MyNaga API (mynaga.app)
```

**How it works:**
1. You configure token in browser
2. Browser sends token to YOUR backend (localhost)
3. YOUR backend connects to MyNaga API
4. MyNaga API returns data
5. YOUR backend stores data locally
6. Browser shows updated data

**No deployment needed!** Everything runs on your computer.

---

## 🔍 Verify Everything is Working

### **Check Backend:**
```bash
# Should return HTML (API docs page)
curl http://127.0.0.1:8000/docs
```

### **Check Frontend:**
```bash
# Should return "Vite v5.x.x ready"
# Frontend should be running on port 3000
```

### **Test MyNaga Connection:**
```bash
curl -X POST "http://127.0.0.1:8000/api/mynaga/test-connection?auth_token=YOUR_TOKEN_HERE"
```

Should return:
```json
{
  "success": true,
  "message": "Connection successful",
  "sample_count": 1
}
```

---

## 🐛 Troubleshooting Steps

### **Problem: Frontend won't load**

**Solution:**
```bash
# Clear cache and restart
cd frontend
rm -rf node_modules/.vite
npm run dev
```

### **Problem: Backend error "module not found"**

**Solution:**
```bash
# Reinstall dependencies
cd backend
python3 -m pip install -r requirements.txt --force-reinstall
```

### **Problem: SSL Certificate Error**

**Solution (Already Done ✅):**
```bash
# Install Python SSL certificates
python3 -m pip install --upgrade certifi
/Applications/Python*/Install\ Certificates.command
```

### **Problem: Port already in use**

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python3 -m uvicorn main:app --reload --port 8001
```

### **Problem: "Connection failed" in dashboard**

**Checklist:**
1. ✅ Backend running? (check http://127.0.0.1:8000/docs)
2. ✅ Token copied correctly? (no "Bearer" prefix)
3. ✅ Internet connection working?
4. ✅ SSL certificates installed?

---

## 🎯 What Should Work Now

### ✅ **On Localhost:**
- Backend API running
- Frontend dashboard loading
- MyNaga connection test passing
- Real-time sync configurable
- Data syncing every 5 minutes
- Manual sync button working

### ❌ **Not Needed:**
- GitHub deployment
- Heroku/AWS deployment
- Public hosting
- Domain name
- SSL certificates for localhost

---

## 📊 Real-Time Sync Features

### **Automatic Sync:**
- Runs every 5 minutes (configurable)
- Background operation
- No manual action needed
- Status tracking
- Error logging

### **Manual Controls:**
- Test connection before sync
- Trigger manual sync anytime
- View sync statistics
- Monitor sync status
- Stop sync if needed

### **Data Flow:**
```
Every 5 Minutes:
  1. Background job wakes up
  2. Connects to MyNaga API
  3. Fetches new reports
  4. Maps to local database
  5. Updates dashboard
  6. Logs statistics
```

---

## 🚀 Quick Start Commands

### **Terminal 1 - Backend:**
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
python3 -m uvicorn main:app --reload --app-dir /Users/jirehb.custodio/Python/mynaga-dashboard/backend
```

### **Terminal 2 - Frontend:**
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/frontend
npm run dev
```

### **Browser:**
```
http://localhost:3000
```

---

## 📞 Still Having Issues?

### **Check These Files:**
- `backend/mynaga_sync.py` - API client (SSL handling added ✅)
- `backend/mynaga_routes.py` - API endpoints
- `backend/scheduler.py` - Background jobs
- `frontend/src/pages/MyNagaSetup.jsx` - Configuration UI

### **Check Logs:**
- Backend terminal - Shows API requests and errors
- Frontend terminal - Shows React errors
- Browser console (F12) - Shows JavaScript errors

### **Test Individual Components:**

**1. Backend Health:**
```bash
curl http://127.0.0.1:8000/
```

**2. API Docs:**
```bash
open http://127.0.0.1:8000/docs
```

**3. Frontend:**
```bash
open http://localhost:3000
```

---

## ✅ Summary

**Your MyNaga Dashboard:**
- ✅ Works on localhost
- ✅ No deployment needed
- ✅ SSL certificates installed
- ✅ Real-time sync ready
- ✅ All features working

**Just Start:**
1. Backend (Terminal 1)
2. Frontend (Terminal 2)
3. Configure token in browser
4. Sync starts automatically! ⚡

---

## 🎉 You're Ready!

**Your dashboard is complete and works on localhost!**

No GitHub, no deployment, no cloud needed. Everything runs on your Mac! 🚀

*Last Updated: October 22, 2025*
*Status: SSL Fixed ✅ | Ready to Use ✅*
