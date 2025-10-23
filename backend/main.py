"""FastAPI main application."""
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import os
import tempfile
import logging

from config import settings
from database import get_db, init_db
from models import Case, Office, Cluster, Tag, CaseUpdate
from schemas import (
    CaseCreate, CaseResponse, CaseUpdate as CaseUpdateSchema,
    OfficeCreate, OfficeResponse,
    ClusterCreate, ClusterResponse, ClusterUpdate,
    TagCreate, TagResponse,
    StatsResponse
)
from excel_importer import ExcelImporter
from mynaga_routes import router as mynaga_router
from google_sheets_routes import router as google_sheets_router

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="MyNaga Dashboard API for managing cases, offices, and clusters"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()
    # Note: MyNaga sync will be initialized via API endpoint /api/mynaga/config


# Include integration routes
app.include_router(mynaga_router)
app.include_router(google_sheets_router)


# ============================================================================
# CASES ENDPOINTS
# ============================================================================

@app.get("/api/cases", response_model=List[CaseResponse])
def get_cases(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10000, ge=1, le=50000),
    status: str = Query(None),
    category: str = Query(None),
    barangay: str = Query(None),
    search: str = Query(None),
):
    """Get all cases with optional filtering."""
    query = db.query(Case)
    
    if status:
        query = query.filter(Case.status == status)
    if category:
        query = query.filter(Case.category == category)
    if barangay:
        query = query.filter(Case.barangay == barangay)
    if search:
        query = query.filter(
            (Case.control_no.ilike(f"%{search}%")) |
            (Case.description.ilike(f"%{search}%")) |
            (Case.reported_by.ilike(f"%{search}%"))
        )
    
    # Order by most recent cases first (by ID descending)
    query = query.order_by(Case.id.desc())
    
    cases = query.offset(skip).limit(limit).all()
    return cases


@app.get("/api/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    """Get a specific case by ID."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.post("/api/cases", response_model=CaseResponse)
def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    """Create a new case."""
    # Check if case already exists
    existing = db.query(Case).filter(Case.control_no == case.control_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Case already exists")
    
    db_case = Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


@app.put("/api/cases/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: int,
    case_update: CaseUpdateSchema,
    db: Session = Depends(get_db)
):
    """Update a case."""
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    update_data = case_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_case, key, value)
    
    db_case.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_case)
    
    # Two-way sync: Write changes back to Google Sheets
    try:
        from scheduler import sync_manager
        from google_sheets_sync import write_case_to_sheet
        
        # Check if Google Sheets is configured
        if sync_manager.sheets_config:
            logger.info(f"Syncing case {db_case.control_no} back to Google Sheets...")
            
            # Prepare case data for writing
            case_data = {
                'control_no': db_case.control_no,
                'category': db_case.category,
                'sender_location': db_case.sender_location,
                'cluster': db_case.cluster or '',  # Column D
                'barangay': db_case.barangay,
                'description': db_case.description,
                'date_created': db_case.date_created.isoformat() if db_case.date_created else '',
                'reported_by': db_case.reported_by or '',
                'contact_number': db_case.contact_number or '',
                'office': db_case.office or '',  # Column I
                'link_to_report': db_case.link_to_report or '',
                'mynaga_app_status': db_case.mynaga_app_status or '',  # Column M
                'updates_sent_to_user': db_case.updates_sent_to_user_new or '',  # Column N (use _new field)
                'status': db_case.status or 'OPEN',
            }
            
            # Write to Google Sheets
            success = write_case_to_sheet(
                case_data=case_data,
                sheet_url=sync_manager.sheets_config.get('sheet_url'),
                credentials_json=sync_manager.sheets_config.get('credentials_json')
            )
            
            if success:
                logger.info(f"✅ Case {db_case.control_no} synced to Google Sheets")
            else:
                logger.warning(f"⚠️ Failed to sync case {db_case.control_no} to Google Sheets")
        else:
            logger.debug("Google Sheets not configured, skipping write-back")
            
    except Exception as e:
        # Don't fail the update if Google Sheets sync fails
        logger.error(f"Error syncing to Google Sheets: {str(e)}")
    
    return db_case


@app.delete("/api/cases/{case_id}")
def delete_case(case_id: int, db: Session = Depends(get_db)):
    """Delete a case."""
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db.delete(db_case)
    db.commit()
    return {"message": "Case deleted"}


# ============================================================================
# OFFICES ENDPOINTS
# ============================================================================

@app.get("/api/offices", response_model=List[OfficeResponse])
def get_offices(db: Session = Depends(get_db)):
    """Get all offices."""
    return db.query(Office).filter(Office.is_active == True).all()


@app.post("/api/offices", response_model=OfficeResponse)
def create_office(office: OfficeCreate, db: Session = Depends(get_db)):
    """Create a new office."""
    db_office = Office(**office.dict())
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office


@app.post("/api/cases/{case_id}/offices/{office_id}")
def assign_office_to_case(
    case_id: int,
    office_id: int,
    db: Session = Depends(get_db)
):
    """Assign an office to a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    office = db.query(Office).filter(Office.id == office_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    
    if office not in case.offices:
        case.offices.append(office)
        db.commit()
    
    return {"message": "Office assigned to case"}


# ============================================================================
# CLUSTERS ENDPOINTS
# ============================================================================

@app.get("/api/clusters", response_model=List[ClusterResponse])
def get_clusters(db: Session = Depends(get_db)):
    """Get all clusters."""
    return db.query(Cluster).all()


@app.post("/api/clusters", response_model=ClusterResponse)
def create_cluster(cluster: ClusterCreate, db: Session = Depends(get_db)):
    """Create a new cluster."""
    db_cluster = Cluster(**cluster.dict())
    db.add(db_cluster)
    db.commit()
    db.refresh(db_cluster)
    return db_cluster


@app.put("/api/clusters/{cluster_id}", response_model=ClusterResponse)
def update_cluster(
    cluster_id: int,
    cluster_update: ClusterUpdate,
    db: Session = Depends(get_db)
):
    """Update a cluster."""
    db_cluster = db.query(Cluster).filter(Cluster.id == cluster_id).first()
    if not db_cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    update_data = cluster_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cluster, key, value)
    
    db_cluster.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_cluster)
    return db_cluster


@app.post("/api/cases/{case_id}/clusters/{cluster_id}")
def assign_cluster_to_case(
    case_id: int,
    cluster_id: int,
    db: Session = Depends(get_db)
):
    """Assign a cluster to a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    cluster = db.query(Cluster).filter(Cluster.id == cluster_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    if cluster not in case.clusters:
        case.clusters.append(cluster)
        db.commit()
    
    return {"message": "Cluster assigned to case"}


# ============================================================================
# TAGS ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/tags", response_model=TagResponse)
def add_tag_to_case(
    case_id: int,
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    """Add a tag to a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db_tag = Tag(case_id=case_id, **tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.delete("/api/tags/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Delete a tag."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}


# ============================================================================
# CASE UPDATES ENDPOINTS
# ============================================================================

@app.post("/api/cases/{case_id}/updates")
def add_case_update(
    case_id: int,
    update: CaseUpdateSchema,
    db: Session = Depends(get_db)
):
    """Add an update to a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db_update = CaseUpdate(case_id=case_id, **update.dict())
    db.add(db_update)
    
    # Update case status if provided
    if update.status_after_update:
        case.status = update.status_after_update
        case.last_status_update_datetime = datetime.utcnow()
    
    db.commit()
    db.refresh(db_update)
    return db_update


# ============================================================================
# FILE IMPORT ENDPOINTS
# ============================================================================

@app.post("/api/import/excel")
async def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Import cases from Excel file."""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel file")
    
    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name
    
    try:
        imported_count, errors = ExcelImporter.import_excel(tmp_path, db)
        return {
            "success": True,
            "imported_count": imported_count,
            "errors": errors
        }
    finally:
        os.unlink(tmp_path)


@app.get("/api/export/excel")
def export_excel(db: Session = Depends(get_db)):
    """Export all cases to Excel file."""
    cases = db.query(Case).all()
    
    export_path = os.path.join(tempfile.gettempdir(), f"mynaga_export_{datetime.utcnow().timestamp()}.xlsx")
    success = ExcelImporter.export_cases(cases, export_path)
    
    if success:
        return {"success": True, "file_path": export_path}
    else:
        raise HTTPException(status_code=500, detail="Error exporting cases")


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@app.get("/api/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    total_cases = db.query(Case).count()
    open_cases = db.query(Case).filter(Case.status == "OPEN").count()
    resolved_cases = db.query(Case).filter(Case.status == "RESOLVED").count()
    rerouting_cases = db.query(Case).filter(Case.status == "FOR REROUTING").count()
    total_offices = db.query(Office).filter(Office.is_active == True).count()
    total_clusters = db.query(Cluster).count()
    
    # Calculate average case aging
    avg_aging = db.query(Case).filter(Case.case_aging != None).all()
    average_case_aging = sum([c.case_aging for c in avg_aging]) / len(avg_aging) if avg_aging else 0
    
    return StatsResponse(
        total_cases=total_cases,
        open_cases=open_cases,
        resolved_cases=resolved_cases,
        rerouting_cases=rerouting_cases,
        total_offices=total_offices,
        total_clusters=total_clusters,
        average_case_aging=average_case_aging
    )


@app.get("/api/mynaga-stats")
def get_mynaga_stats(db: Session = Depends(get_db)):
    """Get MyNaga App Status statistics for real-time dashboard."""
    from sqlalchemy import func
    
    # Get counts for each MyNaga status
    status_counts = db.query(
        Case.mynaga_app_status,
        func.count(Case.id).label('count')
    ).filter(
        Case.mynaga_app_status.isnot(None)
    ).group_by(
        Case.mynaga_app_status
    ).all()
    
    # Create result dictionary with all statuses (default to 0)
    stats = {
        'In Progress': 0,
        'No Status Yet': 0,
        'Pending Confirmation': 0,
        'Rejected': 0,
        'Resolved': 0,
        'Under Review': 0,
        'total': 0
    }
    
    # Fill in actual counts
    for status, count in status_counts:
        if status in stats:
            stats[status] = count
        stats['total'] += count
    
    return stats


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "MyNaga Dashboard API",
        "version": settings.api_version,
        "docs": "/docs"
    }
