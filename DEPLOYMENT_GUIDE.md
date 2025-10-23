# 🚀 Deployment Guide - MyNaga Dashboard

## Overview

Your dashboard has two parts that need different deployment strategies:

### Frontend (React/Vite)
- ✅ **Deploy to Vercel** - Perfect for static sites
- Fast, free, auto-deploys from GitHub

### Backend (FastAPI + Scheduler)
- ⚠️ **Don't use Vercel** - Not suitable for long-running processes
- ✅ **Use Railway, Render, or Fly.io** - Support persistent apps

---

## 🎯 Recommended Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│   Vercel (Frontend) │────────▶│  Railway (Backend)   │
│                     │  HTTPS  │                      │
│  - React app        │         │  - FastAPI           │
│  - Static files     │         │  - SQLite/Postgres   │
│  - CDN delivery     │         │  - Auto-sync job     │
│  - Free tier        │         │  - MyNaga API calls  │
└─────────────────────┘         └──────────────────────┘
         │                               │
         │                               │
         ▼                               ▼
    End Users                    Google Sheets API
                                 MyNaga API
```

---

## 📦 Option 1: Vercel (Frontend) + Railway (Backend)

### **Why This Combo?**
- ✅ Frontend: Lightning fast on Vercel's CDN
- ✅ Backend: Railway supports persistent processes & auto-sync
- ✅ Both have generous free tiers
- ✅ Easy deployment from GitHub

### **Frontend Deployment (Vercel)**

1. **Push code to GitHub:**
   ```bash
   cd /Users/jirehb.custodio/Python/mynaga-dashboard
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/mynaga-dashboard.git
   git push -u origin main
   ```

2. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Click "Import Project"
   - Select your GitHub repo
   - Configure:
     - **Framework Preset:** Vite
     - **Root Directory:** `frontend`
     - **Build Command:** `npm run build`
     - **Output Directory:** `dist`
   - Add Environment Variable:
     ```
     VITE_API_URL=https://your-app-name.railway.app
     ```

3. **Update frontend API calls:**
   ```javascript
   // In your frontend code, replace:
   const API_BASE = "http://localhost:8000"
   
   // With:
   const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000"
   ```

### **Backend Deployment (Railway)**

1. **Create `railway.json`:**
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
       "healthcheckPath": "/api/stats",
       "healthcheckTimeout": 100,
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

2. **Create `Procfile` (in backend folder):**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Update `requirements.txt`:**
   ```bash
   cd backend
   pip freeze > requirements.txt
   ```

4. **Deploy to Railway:**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Configure:
     - **Root Directory:** `backend`
     - **Start Command:** Auto-detected
   - Add Environment Variables:
     - `GOOGLE_SHEETS_CREDENTIALS` (your service account JSON)
     - `SPREADSHEET_ID`
     - `PORT=8000`
   - Deploy!

5. **Enable CORS for your frontend:**
   Update `backend/main.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://your-vercel-app.vercel.app",  # Your Vercel domain
           "http://localhost:3000"  # Local development
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## 📦 Option 2: All-in-One on Render

### **Simpler but slightly slower**

1. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: mynaga-backend
       env: python
       region: singapore
       plan: free
       buildCommand: pip install -r backend/requirements.txt
       startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: GOOGLE_SHEETS_CREDENTIALS
           sync: false
         - key: SPREADSHEET_ID
           sync: false
       
     - type: web
       name: mynaga-frontend
       env: static
       buildCommand: cd frontend && npm install && npm run build
       staticPublishPath: frontend/dist
       routes:
         - type: rewrite
           source: /*
           destination: /index.html
   ```

2. **Deploy:**
   - Push to GitHub
   - Go to https://render.com
   - "New" → "Blueprint"
   - Connect repo
   - Deploy!

---

## 📦 Option 3: Fly.io (Best for Asia/Philippines)

### **Fastest for Philippine users**

1. **Install Fly CLI:**
   ```bash
   brew install flyctl
   fly auth login
   ```

2. **Deploy Backend:**
   ```bash
   cd backend
   fly launch --name mynaga-backend --region sin  # Singapore
   fly secrets set GOOGLE_SHEETS_CREDENTIALS="$(cat credentials.json)"
   fly secrets set SPREADSHEET_ID="your_id"
   fly deploy
   ```

3. **Deploy Frontend:**
   ```bash
   cd frontend
   fly launch --name mynaga-frontend --region sin
   fly deploy
   ```

---

## ⚙️ Code Changes Needed for Production

### 1. **Environment Variables**

Create `backend/config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Environment-based config
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# API URLs
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Database
if IS_PRODUCTION:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./production.db")
else:
    DATABASE_URL = "sqlite:///./test.db"

# Google Sheets
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

# MyNaga API
MYNAGA_TOKEN = os.getenv("MYNAGA_TOKEN")
```

### 2. **Frontend API Configuration**

Create `frontend/.env.production`:
```env
VITE_API_URL=https://your-backend-url.railway.app
```

Create `frontend/.env.development`:
```env
VITE_API_URL=http://localhost:8000
```

Update `frontend/src/config.js`:
```javascript
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### 3. **Update API Calls**

Replace all `http://localhost:8000` with:
```javascript
import { API_BASE_URL } from './config'

// Example:
fetch(`${API_BASE_URL}/api/cases`)
```

### 4. **Database Migration**

For production, consider PostgreSQL instead of SQLite:

```python
# backend/database.py
import os

if os.getenv("DATABASE_URL"):
    # Production: Use Postgres
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")
else:
    # Development: Use SQLite
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
```

---

## 🔒 Security Checklist

Before deploying:

- [ ] **Never commit secrets** - Use environment variables
- [ ] **Update CORS origins** - Only allow your domains
- [ ] **Secure Google credentials** - Store in env vars, not files
- [ ] **Rotate MyNaga token** - Don't hardcode in mynaga_link_service.py
- [ ] **Enable HTTPS** - All platforms provide this free
- [ ] **Add rate limiting** - Prevent API abuse
- [ ] **Secure database** - Use Postgres with strong password

---

## 🚨 Real-Time Sync Considerations

### **Your Current Auto-Sync (APScheduler):**

✅ **Will work on:**
- Railway ✓
- Render ✓
- Fly.io ✓
- Any VPS (DigitalOcean, Linode) ✓

❌ **Won't work on:**
- Vercel (serverless only)
- Netlify (serverless only)
- GitHub Pages (static only)

### **Alternative: Cron Jobs**

If you must use Vercel backend (not recommended), you'd need:

1. **Vercel Cron Functions** (Pro plan only):
   ```javascript
   // api/cron/sync.js
   export default async function handler(req, res) {
     // Call your sync endpoint
     await fetch('https://your-api/api/sync')
     res.status(200).json({ synced: true })
   }
   ```

2. **External cron service:**
   - Use https://cron-job.org to hit your sync endpoint every 10 seconds
   - Not ideal for real-time (adds delay)

---

## 💰 Cost Comparison

| Platform | Free Tier | Real-time Sync | Best For |
|----------|-----------|----------------|----------|
| **Vercel + Railway** | Yes (both) | ✅ Yes | **Recommended** |
| **Render** | Yes (750hrs) | ✅ Yes | Simpler setup |
| **Fly.io** | Yes (3 apps) | ✅ Yes | Asia/PH users |
| **Vercel only** | Yes | ❌ No | Not suitable |

---

## 📝 Deployment Checklist

### Pre-Deployment
- [ ] Test locally with production build
- [ ] Update API URLs to use env variables
- [ ] Add all secrets to `.gitignore`
- [ ] Create `requirements.txt` (backend)
- [ ] Test CORS with different origins
- [ ] Database migration ready

### Frontend (Vercel)
- [ ] Push to GitHub
- [ ] Connect repo to Vercel
- [ ] Set `VITE_API_URL` env var
- [ ] Deploy and test
- [ ] Custom domain (optional)

### Backend (Railway/Render/Fly)
- [ ] Create account
- [ ] Connect GitHub repo
- [ ] Add environment variables:
  - [ ] `GOOGLE_SHEETS_CREDENTIALS`
  - [ ] `SPREADSHEET_ID`
  - [ ] `MYNAGA_TOKEN`
  - [ ] `DATABASE_URL` (if Postgres)
- [ ] Deploy and test
- [ ] Verify auto-sync is running
- [ ] Check logs

### Post-Deployment
- [ ] Test all features end-to-end
- [ ] Verify Google Sheets sync
- [ ] Test MyNaga link fetching
- [ ] Monitor error logs
- [ ] Set up uptime monitoring

---

## 🎯 My Recommendation

**For Philippine Government Use:**

```
Frontend: Vercel (Free)
Backend:  Railway (Free tier, upgrade if needed)
Database: Start with SQLite, migrate to Postgres if scaling

Why?
- ✅ Free to start
- ✅ Easy GitHub integration
- ✅ Auto-sync works perfectly
- ✅ Can scale later
- ✅ Professional setup
```

**Quick Start:**
1. Push code to GitHub (10 min)
2. Deploy frontend to Vercel (5 min)
3. Deploy backend to Railway (10 min)
4. Update environment variables (5 min)
5. Test! (15 min)

**Total time: ~45 minutes** 🚀

---

## 🆘 Troubleshooting

### "Auto-sync not working in production"
- Check logs for scheduler startup
- Verify Railway/Render keeps process running
- Not using Vercel for backend, right?

### "CORS errors"
- Update `allow_origins` in main.py
- Add your Vercel domain
- Redeploy backend

### "Google Sheets sync fails"
- Check env var `GOOGLE_SHEETS_CREDENTIALS` is set
- Verify JSON is valid (no line breaks)
- Check service account has Sheet access

### "MyNaga links not working"
- Update `MYNAGA_TOKEN` env var
- Check token hasn't expired
- Verify SSL context works in production

---

## 📚 Resources

- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

**Need help deploying? Let me know which platform you prefer and I'll guide you through the specific steps!** 🚀
