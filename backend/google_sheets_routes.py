"""Google Sheets sync API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from typing import Optional
from google_sheets_sync import sync_from_google_sheets

router = APIRouter(prefix="/api/google-sheets", tags=["Google Sheets"])


class GoogleSheetsConfig(BaseModel):
    """Google Sheets configuration."""
    sheet_url: str
    credentials_json: Optional[str] = None


class SyncRequest(BaseModel):
    """Sync request with sheet URL."""
    sheet_url: str
    credentials_json: Optional[str] = None


@router.post("/test-connection")
async def test_google_sheets_connection(config: GoogleSheetsConfig):
    """
    Test connection to Google Sheets.
    
    Args:
        config: Google Sheets configuration
        
    Returns:
        Connection test result
    """
    try:
        from google_sheets_sync import GoogleSheetsSync
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            syncer = GoogleSheetsSync(
                config.sheet_url, 
                db, 
                credentials_json=config.credentials_json
            )
            rows = await syncer.fetch_sheet_data()
            
            auth_method = "Service Account (Private)" if config.credentials_json else "Published CSV"
            
            return {
                "success": True,
                "message": f"Successfully connected to Google Sheets via {auth_method}",
                "row_count": len(rows),
                "columns": list(rows[0].keys()) if rows else [],
                "auth_method": auth_method
            }
        finally:
            db.close()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")


@router.post("/sync")
async def sync_google_sheets(request: SyncRequest, db: Session = Depends(get_db)):
    """
    Sync data from Google Sheets to database.
    
    Args:
        request: Sync request with sheet URL and optional credentials
        db: Database session
        
    Returns:
        Sync statistics
    """
    try:
        from google_sheets_sync import GoogleSheetsSync
        
        syncer = GoogleSheetsSync(
            request.sheet_url, 
            db,
            credentials_json=request.credentials_json
        )
        stats = await syncer.sync_to_database()
        
        return {
            "success": True,
            "message": f"Synced {stats['created']} new cases, updated {stats['updated']} existing cases",
            "stats": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.get("/status")
def get_sync_status():
    """Get Google Sheets sync status including auto-sync info."""
    from scheduler import sync_manager
    status = sync_manager.get_sync_status()
    return status.get("google_sheets", {})


class AutoSyncConfig(BaseModel):
    """Auto-sync configuration."""
    sheet_url: str
    credentials_json: Optional[str] = None
    interval_seconds: int = 10  # Changed to seconds for faster refresh


@router.post("/auto-sync/start")
async def start_auto_sync(config: AutoSyncConfig):
    """
    Start automatic Google Sheets sync.
    
    Args:
        config: Auto-sync configuration with sheet URL and interval
        
    Returns:
        Success message
    """
    try:
        from scheduler import init_google_sheets_scheduler
        
        # Pass the full sheet_url (not just the ID)
        result = init_google_sheets_scheduler(
            sheet_url=config.sheet_url,
            credentials_json=config.credentials_json,
            sync_interval_seconds=config.interval_seconds
        )
        
        return {
            "success": True,
            "message": f"Auto-sync started: syncing every {config.interval_seconds} seconds",
            "details": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start auto-sync: {str(e)}")


@router.post("/auto-sync/stop")
async def stop_auto_sync():
    """
    Stop automatic Google Sheets sync.
    
    Returns:
        Success message
    """
    try:
        from scheduler import stop_google_sheets_scheduler
        
        result = stop_google_sheets_scheduler()
        
        return {
            "success": True,
            "message": "Auto-sync stopped",
            "details": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop auto-sync: {str(e)}")
