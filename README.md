# MyNaga Dashboard

A comprehensive web application for managing cases, offices, and clusters from MyNaga reports. Features real-time data tracking, user-friendly tagging and clustering, and Excel import/export capabilities.

## Features

✅ **Case Management**
- Create, read, update, and delete cases
- Track case status (OPEN, RESOLVED, FOR REROUTING)
- Assign offices and clusters to cases
- Add tags and status updates to cases

✅ **Real-time MyNaga Integration** ⭐ NEW
- Auto-sync data directly from MyNaga App API
- No manual Excel imports needed
- Automatic background synchronization (configurable interval)
- Test connection before enabling
- View sync status and history

✅ **Office Management**
- Manage office information
- Assign cases to offices
- Track office assignments

✅ **Clustering & Organization**
- Create and manage clusters
- Assign multiple cases to clusters
- Color-coded clusters for easy identification
- Organize by barangay

✅ **Data Import/Export**
- Import cases from Excel files
- Export all cases to Excel
- Automatic data validation

✅ **Real-time Dashboard**
- View key statistics
- Track case aging
- Monitor resolution rates
- Visual charts and graphs

## Project Structure

```
mynaga-dashboard/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI application
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic validation schemas
│   ├── database.py            # Database connection
│   ├── excel_importer.py      # Excel file handling
│   ├── config.py              # Configuration settings
│   └── requirements.txt        # Python dependencies
│
└── frontend/                   # React + Vite frontend
    ├── src/
    │   ├── components/        # Reusable React components
    │   ├── pages/            # Page components
    │   ├── services/         # API service layer
    │   ├── store/            # Zustand state management
    │   ├── App.jsx           # Main app component
    │   └── index.css          # Tailwind styles
    ├── package.json           # Node dependencies
    ├── vite.config.js         # Vite configuration
    └── tailwind.config.js     # Tailwind CSS config
```

## Tech Stack

**Backend:**
- Python 3.8+
- FastAPI (modern web framework)
- SQLAlchemy (ORM)
- PostgreSQL / SQLite (database)
- Pandas (data processing)
- Openpyxl (Excel handling)

**Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- Zustand (state management)
- Axios (HTTP client)
- Recharts (charting library)

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL (optional, SQLite is default)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd mynaga-dashboard/backend
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. (Optional) Update database URL in `.env`:
```
DATABASE_URL=sqlite:///./mynaga.db
```

6. Run the server:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd mynaga-dashboard/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Using Both Together

1. Start the backend server (Terminal 1):
```bash
cd mynaga-dashboard/backend
source venv/bin/activate
uvicorn main:app --reload
```

2. Start the frontend server (Terminal 2):
```bash
cd mynaga-dashboard/frontend
npm run dev
```

3. Open `http://localhost:3000` in your browser

## API Endpoints

### Cases
- `GET /api/cases` - Get all cases with filtering
- `GET /api/cases/{id}` - Get specific case
- `POST /api/cases` - Create new case
- `PUT /api/cases/{id}` - Update case
- `DELETE /api/cases/{id}` - Delete case
- `POST /api/cases/{id}/updates` - Add status update
- `POST /api/cases/{id}/offices/{office_id}` - Assign office
- `POST /api/cases/{id}/clusters/{cluster_id}` - Assign cluster
- `POST /api/cases/{id}/tags` - Add tag

### Offices
- `GET /api/offices` - Get all offices
- `POST /api/offices` - Create office

### Clusters
- `GET /api/clusters` - Get all clusters
- `POST /api/clusters` - Create cluster
- `PUT /api/clusters/{id}` - Update cluster

### File Import/Export
- `POST /api/import/excel` - Import cases from Excel
- `GET /api/export/excel` - Export cases to Excel

### Statistics
- `GET /api/stats` - Get dashboard statistics

## Usage Guide

### Importing Data

1. Go to the **Cases** page
2. Click **Import Excel** button
3. Select your Excel file
4. The system will validate and import all cases
5. Any errors will be displayed

### Creating a New Case

1. Click **New Case** button
2. Fill in the required fields (Control No., Category)
3. Add optional information (location, description, etc.)
4. Click **Create Case**

### Managing Clusters

1. Create a cluster with a name, color, and barangay
2. Assign cases to clusters
3. Use clusters for organizing related cases
4. Color-coding helps with visual organization

### Tagging Cases

1. Open a case
2. Add tags for custom categorization
3. Use tags for filtering and searching
4. Tags help with quick identification

### Tracking Status

1. View case status on the dashboard
2. Update status when case progresses
3. Add update notes for tracking
4. Monitor case aging metrics

## Database Schema

### Cases Table
Stores all case/report information including:
- Control number (unique identifier)
- Category and refined category
- Location and barangay information
- Description and attachments
- Reporter information
- Status tracking
- Case aging metrics

### Offices Table
Stores office information:
- Office name and code
- Location
- Contact person and details
- Active status

### Clusters Table
Stores cluster/grouping information:
- Cluster name
- Description
- Color coding
- Barangay association
- Creation metadata

### Tags Table
Stores custom tags for cases:
- Tag name
- Associated case
- Creation timestamp

### Case Updates Table
Stores status update history:
- Update text
- Updated by (user)
- Status after update
- Timestamp

## Configuration

### Database Selection

**SQLite (Default - No setup required):**
```python
DATABASE_URL=sqlite:///./mynaga.db
```

**PostgreSQL:**
```bash
# Install PostgreSQL locally or use cloud service

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/mynaga_dashboard
```

## Development Tips

### Adding New Features

1. **Backend**: Add endpoints in `main.py`, update `schemas.py` for validation
2. **Frontend**: Create components in `src/components/`, add pages in `src/pages/`
3. **State**: Use Zustand stores in `src/store/index.js`
4. **API**: Add service methods in `src/services/api.js`

### Running Tests

```bash
# Backend
pytest

# Frontend
npm test
```

### Building for Production

**Backend:**
```bash
# Set environment to production
export ENVIRONMENT=production
export DEBUG=false

uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
npm run build
```

## Deployment

### Backend Deployment (Example: Heroku)

```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy to Heroku
heroku create mynaga-dashboard-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Frontend Deployment (Example: Vercel)

```bash
npm install -g vercel
vercel
```

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify Python virtual environment is activated
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't connect to backend
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `main.py`
- Check browser console for errors (F12)

### Import Excel fails
- Verify Excel file has required columns
- Ensure Control No. is unique
- Check file format (.xlsx or .xls)

### Database errors
- Delete `mynaga.db` if using SQLite to reset database
- Run migrations for PostgreSQL
- Check database URL in `.env`

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -am 'Add my feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Submit a pull request

## License

MIT License - feel free to use this for your projects

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

Built with ❤️ for MyNaga case management
