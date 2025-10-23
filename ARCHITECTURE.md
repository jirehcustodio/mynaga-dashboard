# MyNaga Dashboard - Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          WEB BROWSER                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    FRONTEND (React)                        │ │
│  │                                                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │ │
│  │  │Dashboard │  │Cases     │  │Clusters  │               │ │
│  │  │(Stats)   │  │(Management)│ │(Organization)            │ │
│  │  └──────────┘  └──────────┘  └──────────┘               │ │
│  │         │              │              │                  │ │
│  │  ┌──────────────────────────────────────────────┐       │ │
│  │  │     Zustand State Management                 │       │ │
│  │  │  (Cases, Offices, Clusters, Stats)          │       │ │
│  │  └──────────────────────────────────────────────┘       │ │
│  │         │                                               │ │
│  │  ┌──────────────────────────────────────────────┐       │ │
│  │  │     Axios API Client                         │       │ │
│  │  │     (HTTP Requests to Backend)               │       │ │
│  │  └──────────────────────────────────────────────┘       │ │
│  │         │                                               │ │
│  └─────────┼───────────────────────────────────────────────┘ │
│            │                                                   │
└────────────┼───────────────────────────────────────────────────┘
             │ HTTP/REST
             │
┌────────────┼───────────────────────────────────────────────────┐
│            ▼                                                    │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │          BACKEND (FastAPI - Python)                    │  │
│  │                                                         │  │
│  │  ┌────────────────────────────────────────────────────┐│  │
│  │  │              API Routes (25+ Endpoints)            ││  │
│  │  │                                                    ││  │
│  │  │  GET/POST/PUT/DELETE /api/cases                  ││  │
│  │  │  GET/POST /api/offices                           ││  │
│  │  │  GET/POST/PUT /api/clusters                      ││  │
│  │  │  POST /api/import/excel                          ││  │
│  │  │  GET /api/stats                                  ││  │
│  │  └────────────────────────────────────────────────────┘│  │
│  │         │                │                │            │  │
│  │  ┌──────▼───┐   ┌────────▼──────┐  ┌────▼─────────┐ │  │
│  │  │ Service  │   │ Excel Importer│  │ Validators  │ │  │
│  │  │ Logic    │   │ (Pandas)      │  │ (Pydantic)  │ │  │
│  │  └──────────┘   └───────────────┘  └─────────────┘ │  │
│  │         │                │                │         │  │
│  │  ┌──────┴────────────────┴────────────────┴─────┐  │  │
│  │  │     SQLAlchemy ORM Layer                     │  │  │
│  │  │   (Database abstraction)                     │  │  │
│  │  └──────┬───────────────────────────────────────┘  │  │
│  └─────────┼──────────────────────────────────────────┘  │
│            │                                              │
└────────────┼──────────────────────────────────────────────┘
             │ SQL
             │
┌────────────┼──────────────────────────────────────────────────┐
│            ▼                                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              DATABASE                                    │ │
│  │                                                          │ │
│  │  SQLite / PostgreSQL                                    │ │
│  │                                                          │ │
│  │  Tables:                                                │ │
│  │  • cases (Main data)                                   │ │
│  │  • offices                                             │ │
│  │  • clusters                                            │ │
│  │  • tags                                                │ │
│  │  • case_updates                                        │ │
│  │  • case_office_association (Many-to-many)             │ │
│  │  • case_cluster_association (Many-to-many)            │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Creating a Case

```
User Input (Form)
    │
    ▼
CaseModal Component
    │
    ├─► Validates input (Client-side)
    │
    ▼
Axios API Call (POST /api/cases)
    │
    ▼
Backend: create_case() endpoint
    │
    ├─► Validate with Pydantic
    ├─► Check for duplicates
    │
    ▼
SQLAlchemy ORM
    │
    ├─► Create Case object
    ├─► Commit to database
    │
    ▼
Database
    │
    └─► Insert into cases table
    
    ▼
Response JSON
    │
    ▼
Zustand Store (useCaseStore.addCase)
    │
    ▼
UI Re-render
    │
    ▼
Display in Cases Table
```

### Importing Excel

```
User selects file
    │
    ▼
File validation (xlsx/xls)
    │
    ▼
Upload via Axios
    │
    ▼
Backend: import_excel() endpoint
    │
    ├─► Save temp file
    │
    ▼
ExcelImporter class
    │
    ├─► Read with Pandas
    ├─► Map columns to database
    ├─► Validate each row
    ├─► Check for duplicates
    │
    ▼
For each case:
    │
    ├─► Create or Update
    ├─► Handle relationships
    │
    ▼
Database
    │
    └─► Bulk insert/update
    
    ▼
Response (count + errors)
    │
    ▼
Reload cases from API
    │
    ▼
Update Zustand store
    │
    ▼
Show import summary
```

### Filtering & Search

```
User inputs search/filter
    │
    ▼
Zustand store updates filters
    │
    ▼
useEffect triggers
    │
    ▼
Axios GET /api/cases?filters
    │
    ▼
Backend builds query
    │
    ├─► Filter by status
    ├─► Filter by category
    ├─► Filter by barangay
    ├─► Search text (ilike)
    │
    ▼
Database executes query
    │
    ▼
Return filtered results
    │
    ▼
Update Zustand state
    │
    ▼
CaseTable re-renders
    │
    ▼
Show filtered results
```

---

## Database Schema Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                          CASES                              │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                      │
│ control_no (UK) - Unique identifier                         │
│ date_created                                                 │
│ category                                                     │
│ sender_location                                              │
│ barangay                                                     │
│ description                                                  │
│ status (OPEN/RESOLVED/FOR REROUTING)                        │
│ reported_by                                                  │
│ contact_number                                               │
│ ... (30+ more fields)                                       │
└──────────────────────┬──────────────────────┬───────────────┘
                       │                      │
         ┌─────────────┘                      └──────────────┐
         │                                                    │
    One-to-Many                                          One-to-Many
         │                                                    │
         ▼                                                    ▼
┌──────────────────────┐                           ┌──────────────────┐
│   CASE_UPDATES       │                           │    TAGS          │
├──────────────────────┤                           ├──────────────────┤
│ id (PK)              │                           │ id (PK)          │
│ case_id (FK)         │                           │ case_id (FK)     │
│ update_text          │                           │ tag_name         │
│ updated_by           │                           │ created_at       │
│ update_timestamp     │                           └──────────────────┘
│ status_after_update  │
└──────────────────────┘

    Many-to-Many Relationships:

┌────────────────────────────────────┐
│  CASE_OFFICE_ASSOCIATION           │
├────────────────────────────────────┤
│ case_id (FK) ──┐                   │
│ office_id (FK)─┼─┐                 │
└────────────────────────────────────┘
                 │ │
        ┌────────┘ └────────┐
        │                   │
        ▼                   ▼
    ┌─────────────┐    ┌──────────────┐
    │   CASES     │    │   OFFICES    │
    └─────────────┘    ├──────────────┤
                       │ id (PK)      │
                       │ name         │
                       │ location     │
                       │ is_active    │
                       └──────────────┘

┌────────────────────────────────────┐
│  CASE_CLUSTER_ASSOCIATION          │
├────────────────────────────────────┤
│ case_id (FK) ──┐                   │
│ cluster_id(FK)─┼─┐                 │
└────────────────────────────────────┘
                 │ │
        ┌────────┘ └────────┐
        │                   │
        ▼                   ▼
    ┌─────────────┐    ┌──────────────┐
    │   CASES     │    │  CLUSTERS    │
    └─────────────┘    ├──────────────┤
                       │ id (PK)      │
                       │ name         │
                       │ color        │
                       │ barangay     │
                       │ created_by   │
                       └──────────────┘
```

---

## Component Tree

```
App.jsx
│
├── Sidebar.jsx
│   ├── Home Link
│   ├── Cases Link
│   ├── Clusters Link
│   └── Offices Link
│
└── Routes
    │
    ├── Dashboard.jsx
    │   ├── StatCard x 6
    │   ├── BarChart (Cases by Status)
    │   └── Statistics Panel
    │
    └── CasesPage.jsx
        ├── Header
        │   ├── Import Button
        │   └── New Case Button
        │
        ├── SearchBar
        │   └── Filters
        │
        └── CaseTable.jsx
            ├── TableHeader
            ├── TableRows
            │   ├── Edit Button
            │   └── Delete Button
            │
            └── CaseModal.jsx
                ├── Form Fields
                ├── Cancel Button
                └── Submit Button
```

---

## User Workflows

### Workflow 1: Import & Organize

```
1. Start App
   │
   ├─► Go to Cases page
   │
   ├─► Click "Import Excel"
   │
   ├─► Select your data file
   │
   ├─► System imports and validates
   │
   ├─► View import summary
   │
   ├─► See cases in table
   │
   ├─► Go to Clusters page
   │
   ├─► Create clusters
   │
   └─► Assign cases to clusters
```

### Workflow 2: Track & Update

```
1. Open Cases page
   │
   ├─► Click on case
   │
   ├─► Edit form opens
   │
   ├─► Change status
   │
   ├─► Add notes/updates
   │
   ├─► Save changes
   │
   ├─► View on Dashboard
   │
   └─► Statistics update
```

### Workflow 3: Search & Filter

```
1. Open Cases page
   │
   ├─► Type in search bar
   │
   ├─► Select status filter
   │
   ├─► Select category filter
   │
   ├─► Select barangay filter
   │
   ├─► Results filter in real-time
   │
   └─► View filtered cases
```

### Workflow 4: Export Data

```
1. Open Cases page
   │
   ├─► (All cases already visible)
   │
   ├─► Click "Export Excel"
   │
   ├─► File downloads
   │
   └─► Use for reports/backup
```

---

## Deployment Architecture

### Development

```
Your Computer
├─ Backend (localhost:8000)
│  ├─ Python Virtual Environment
│  ├─ Uvicorn Server
│  └─ SQLite Database
│
├─ Frontend (localhost:3000)
│  ├─ Vite Dev Server
│  ├─ Hot Module Reload
│  └─ Browser
```

### Production (Docker)

```
Host Server
│
├─ Docker Daemon
│  │
│  ├─ Backend Container
│  │  ├─ Python App
│  │  ├─ Uvicorn Server
│  │  └─ SQLite/PostgreSQL Client
│  │
│  ├─ Frontend Container
│  │  ├─ Node.js App
│  │  ├─ Serve (Static Files)
│  │  └─ Nginx (Optional)
│  │
│  ├─ Network Bridge
│  └─ Volumes (Data Persistence)
│
└─ Database
   └─ PostgreSQL (Optional, External)
```

### Production (Distributed)

```
Internet
   │
   ├─► CDN (Frontend Static Files)
   │   └─ Vercel / CloudFront
   │
   ├─► API Gateway
   │   └─ Load Balancer
   │
   ├─► Application Servers (Backend)
   │   ├─ Server 1 (Heroku / EC2)
   │   ├─ Server 2
   │   └─ Server 3
   │
   ├─► Database
   │   ├─ Primary PostgreSQL
   │   └─ Replica (Read-only)
   │
   └─► Storage
       └─ S3 / Cloud Storage (Backups)
```

---

## API Request/Response Flow

### Create Case Example

```
REQUEST:
┌─────────────────────────────────────────┐
│ POST /api/cases                         │
│ Content-Type: application/json          │
│                                         │
│ {                                       │
│   "control_no": "CN-2024-001",         │
│   "category": "Water Issue",           │
│   "barangay": "San Isidro",            │
│   "description": "No water supply",    │
│   "status": "OPEN"                     │
│ }                                       │
└─────────────────────────────────────────┘
           │
           ▼ (HTTP POST)
    Backend Processing
           │
           ├─► Pydantic Validation
           ├─► Check Duplicates
           ├─► Create Object
           └─► Save to DB
           │
           ▼
RESPONSE:
┌─────────────────────────────────────────┐
│ HTTP 200 OK                             │
│ Content-Type: application/json          │
│                                         │
│ {                                       │
│   "id": 42,                             │
│   "control_no": "CN-2024-001",         │
│   "category": "Water Issue",           │
│   "barangay": "San Isidro",            │
│   "status": "OPEN",                    │
│   "created_at": "2024-10-22T...",      │
│   "updated_at": "2024-10-22T...",      │
│   "tags": [],                           │
│   "updates": [],                        │
│   "offices": []                         │
│ }                                       │
└─────────────────────────────────────────┘
```

---

**This is a production-ready, fully-featured case management system!** 🚀
