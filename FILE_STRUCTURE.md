# File Structure & Locations

Complete directory tree of your MyNaga Dashboard project:

```
/Users/jirehb.custodio/Python/mynaga-dashboard/
│
├── README.md                          # Main documentation (comprehensive guide)
├── QUICKSTART.md                      # 5-minute setup guide
├── DEPLOYMENT.md                      # Production deployment guide
├── ARCHITECTURE.md                    # System architecture & diagrams
├── PROJECT_OVERVIEW.md                # Project overview & tech stack
│
├── docker-compose.yml                 # Docker orchestration
│
├── backend/                           # 🔵 BACKEND - Python FastAPI
│   ├── main.py                        # ⭐ Main FastAPI application (25+ endpoints)
│   ├── models.py                      # Database models (7 models, 35+ columns)
│   ├── schemas.py                     # Pydantic validation schemas
│   ├── database.py                    # Database connection & session management
│   ├── excel_importer.py              # Excel file import/export logic
│   ├── config.py                      # Configuration management
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                   # Environment variables template
│   ├── Dockerfile                     # Backend containerization
│   └── mynaga.db                      # SQLite database (created on first run)
│
└── frontend/                          # 🟢 FRONTEND - React + Vite
    ├── package.json                   # Node.js dependencies & scripts
    ├── vite.config.js                 # Vite build configuration
    ├── tailwind.config.js             # Tailwind CSS customization
    ├── postcss.config.js              # PostCSS configuration
    ├── index.html                     # HTML entry point
    ├── Dockerfile                     # Frontend containerization
    │
    ├── src/
    │   ├── App.jsx                    # Main React app component
    │   ├── main.jsx                   # React entry point
    │   ├── index.css                  # Tailwind CSS + global styles
    │   │
    │   ├── components/                # Reusable components
    │   │   ├── Sidebar.jsx            # Navigation sidebar
    │   │   ├── CaseModal.jsx          # Case creation/edit form
    │   │   └── CaseTable.jsx          # Cases data table
    │   │
    │   ├── pages/                     # Page components
    │   │   ├── Dashboard.jsx          # Statistics dashboard
    │   │   └── CasesPage.jsx          # Cases management page
    │   │
    │   ├── services/                  # API communication
    │   │   └── api.js                 # Axios API client (25+ endpoints)
    │   │
    │   └── store/                     # State management
    │       └── index.js               # Zustand stores (4 stores)
    │
    └── node_modules/                  # Dependencies (created after npm install)
```

---

## Quick File Reference

### Backend Files to Know

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | All API endpoints | 400+ |
| `models.py` | Database schema | 140+ |
| `schemas.py` | Request validation | 200+ |
| `excel_importer.py` | Excel handling | 150+ |
| `requirements.txt` | Dependencies | 15 |

### Frontend Files to Know

| File | Purpose | Lines |
|------|---------|-------|
| `App.jsx` | Main app routing | 50+ |
| `src/services/api.js` | API client | 50+ |
| `src/store/index.js` | State management | 100+ |
| `components/CaseModal.jsx` | Form component | 100+ |
| `pages/Dashboard.jsx` | Dashboard page | 100+ |

### Documentation Files

| File | Content |
|------|---------|
| `README.md` | Full guide & features |
| `QUICKSTART.md` | 5-minute setup |
| `DEPLOYMENT.md` | Production guide |
| `ARCHITECTURE.md` | System diagrams |
| `PROJECT_OVERVIEW.md` | Tech stack info |

---

## How to Access Your Project

### Location
```
/Users/jirehb.custodio/Python/mynaga-dashboard/
```

### Open in VS Code
```bash
code /Users/jirehb.custodio/Python/mynaga-dashboard
```

### Run Backend
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/backend
source venv/bin/activate
uvicorn main:app --reload
```

### Run Frontend
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard/frontend
npm run dev
```

### Run with Docker
```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard
docker-compose up -d
```

---

## Total Code Lines

### Backend
- FastAPI app: 400+ lines
- Models: 140+ lines
- Schemas: 200+ lines
- Excel importer: 150+ lines
- Database: 30+ lines
- Config: 20+ lines
- **Total Backend: 940+ lines of Python**

### Frontend
- App component: 50+ lines
- Dashboard: 100+ lines
- Cases page: 100+ lines
- Case modal: 100+ lines
- Case table: 50+ lines
- API service: 50+ lines
- Zustand stores: 100+ lines
- Sidebar: 50+ lines
- Styles: 80+ lines
- **Total Frontend: 680+ lines of React/JSX**

### Configuration
- docker-compose.yml: 30 lines
- Backend Dockerfile: 20 lines
- Frontend Dockerfile: 20 lines
- vite.config.js: 15 lines
- tailwind.config.js: 20 lines
- postcss.config.js: 8 lines
- **Total Config: 113 lines**

### Documentation
- README.md: 300+ lines
- QUICKSTART.md: 150+ lines
- DEPLOYMENT.md: 200+ lines
- ARCHITECTURE.md: 250+ lines
- PROJECT_OVERVIEW.md: 200+ lines
- **Total Docs: 1,100+ lines**

**Grand Total: 2,843+ lines of code & documentation**

---

## Database Schema Summary

### 7 Tables Created

1. **cases** (35+ columns)
   - Main case/report data
   - Status tracking
   - Location info
   - Reporter details

2. **offices** (6 columns)
   - Office information
   - Contact details
   - Active status

3. **clusters** (8 columns)
   - Case groupings
   - Color coding
   - Barangay association

4. **tags** (3 columns)
   - Custom tagging
   - Timestamps

5. **case_updates** (5 columns)
   - Status change history
   - Update tracking

6. **case_office_association** (2 columns)
   - Many-to-many relationship

7. **case_cluster_association** (2 columns)
   - Many-to-many relationship

---

## API Endpoints Summary

### Total: 25+ Endpoints

**Cases (7 endpoints)**
- GET /api/cases - List with filtering
- GET /api/cases/{id} - Get one
- POST /api/cases - Create
- PUT /api/cases/{id} - Update
- DELETE /api/cases/{id} - Delete
- POST /api/cases/{id}/updates - Add update
- POST /api/cases/{id}/offices/{office_id} - Assign office
- POST /api/cases/{id}/clusters/{cluster_id} - Assign cluster
- POST /api/cases/{id}/tags - Add tag

**Offices (2 endpoints)**
- GET /api/offices - List
- POST /api/offices - Create

**Clusters (3 endpoints)**
- GET /api/clusters - List
- POST /api/clusters - Create
- PUT /api/clusters/{id} - Update

**Tags (1 endpoint)**
- DELETE /api/tags/{id} - Delete

**Files (2 endpoints)**
- POST /api/import/excel - Import
- GET /api/export/excel - Export

**Stats (1 endpoint)**
- GET /api/stats - Get statistics

---

## Dependencies Installed

### Backend (15 packages)
- fastapi - Web framework
- uvicorn - ASGI server
- sqlalchemy - ORM
- psycopg2-binary - PostgreSQL driver
- python-dotenv - Environment config
- openpyxl - Excel handling
- pandas - Data processing
- pydantic - Validation
- aiofiles - Async file handling
- websockets - Real-time
- requests - HTTP client
- beautifulsoup4 - Web scraping

### Frontend (13 packages)
- react - UI framework
- react-dom - DOM rendering
- react-router-dom - Routing
- axios - HTTP client
- zustand - State management
- react-icons - Icon library
- @headlessui/react - UI components
- @tailwindcss/forms - Form styling
- recharts - Charts
- date-fns - Date utilities
- lodash-es - Utilities

---

## Your Spreadsheet Columns → Database Fields

All columns from your spreadsheet are automatically mapped:

| Spreadsheet Column | Database Field | Type |
|-------------------|---------------|------|
| Control No. | control_no | String (Primary) |
| Date Created | date_created | DateTime |
| Category | category | String |
| Cluster | clusters | Relationship |
| Sender's Location | sender_location | String |
| Barangay | barangay | String |
| Description | description | Text |
| Attached Media | attached_media | String |
| Office | offices | Relationship |
| Reported by | reported_by | String |
| Contact Number | contact_number | String |
| Link to Report | link_to_report | String |
| MyNaga App Status | mynaga_app_status | String |
| Updates Sent to User | updates_sent_to_user | Boolean |
| Office Progress Updates | office_progress_updates | Text |
| Brgy From Cluster | brgy_from_cluster | String |
| Hours Before Deployed | hours_before_deployed | Integer |
| Last Status Update | last_status_update_datetime | DateTime |
| Screened By | screened_by | String |
| Status | status | String (OPEN/RESOLVED/REROUTING) |
| Updates Sent | updates_sent | Boolean |
| Case Aging | case_aging | Integer |
| Month | month | String |
| Feedback Marked | feedback_marked | Boolean |
| Refined Category | refined_category | String |

---

## Next Steps

1. **Read QUICKSTART.md** - Get running in 5 minutes
2. **Import your data** - Upload your Excel file
3. **Create clusters** - Organize your cases
4. **Start using** - Manage and track cases
5. **Check DEPLOYMENT.md** - When ready to deploy

---

**Your MyNaga Dashboard is ready! 🚀**

Questions? Check the documentation files in the project root.
