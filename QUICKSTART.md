# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Backend Setup

```bash
# Navigate to backend
cd mynaga-dashboard/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

**✅ Backend running at:** `http://localhost:8000`
**📚 API Docs:** `http://localhost:8000/docs`

---

### Step 2: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd mynaga-dashboard/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**✅ Frontend running at:** `http://localhost:3000`

---

## 📋 What's Included

### Backend Features
- ✅ FastAPI with automatic API documentation
- ✅ SQLAlchemy ORM with SQLite database
- ✅ Excel file import/export
- ✅ CORS enabled for frontend
- ✅ Case management API
- ✅ Office & cluster management
- ✅ Tag & status update tracking

### Frontend Features
- ✅ React 18 + Vite (fast dev server)
- ✅ Tailwind CSS for styling
- ✅ Zustand for state management
- ✅ Real-time statistics dashboard
- ✅ Case management interface
- ✅ Excel file upload
- ✅ Search & filtering

---

## 📊 Excel Import Format

Your Excel file should have these columns:

```
Control No. | Category | Sender's Location | Barangay | Description | ... (other columns)
```

**Required columns:**
- Control No.
- Category
- Sender's Location
- Barangay
- Description

**Optional columns (automatically recognized):**
- Date Created
- Office
- Reported by
- Contact Number
- Link to Report
- MyNaga App Status
- Status (OPEN/RESOLVED/FOR REROUTING)
- Refined Category
- Any other columns from your spreadsheet

---

## 🔄 API Examples

### Get All Cases
```bash
curl http://localhost:8000/api/cases
```

### Create a New Case
```bash
curl -X POST http://localhost:8000/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "control_no": "CN001",
    "category": "Water Issue",
    "barangay": "San Isidro"
  }'
```

### Import Excel File
```bash
curl -X POST http://localhost:8000/api/import/excel \
  -F "file=@Sheet.xlsx"
```

### Get Statistics
```bash
curl http://localhost:8000/api/stats
```

---

## 🎨 Customization

### Change Database
Edit `backend/config.py`:
```python
# SQLite (default)
database_url: str = "sqlite:///./mynaga.db"

# PostgreSQL
database_url: str = "postgresql://user:password@localhost:5432/mynaga_dashboard"
```

### Change Colors
Edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: "#YOUR_COLOR",
      secondary: "#YOUR_COLOR",
    }
  }
}
```

---

## 🆘 Common Issues

**Port 8000 already in use?**
```bash
uvicorn main:app --reload --port 8001
```

**npm install fails?**
```bash
# Clear npm cache
npm cache clean --force
npm install
```

**"Module not found" errors?**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📱 Next Steps

1. **Import your data**: Upload your existing spreadsheet via the Import Excel button
2. **Create clusters**: Organize cases by location/issue type
3. **Tag cases**: Add custom tags for easy filtering
4. **Track progress**: Update case status and add notes
5. **Monitor metrics**: View dashboard for statistics

---

## 🚢 Production Deployment

### Backend (Example: Railway)
1. Create Railway account
2. Connect GitHub repository
3. Deploy automatically

### Frontend (Example: Vercel)
1. Create Vercel account
2. Connect GitHub repository
3. Deploy automatically

---

## 💡 Pro Tips

- 📤 Export cases to Excel anytime for backups
- 🏷️ Use tags for quick categorization
- 🎯 Assign multiple offices to a case
- 📊 Check dashboard for insights
- 🔍 Use search to find specific cases
- 💾 Bulk import from Excel saves time

---

**🎉 You're all set! Start managing your cases today.**

Questions? Check the README.md for more details!
