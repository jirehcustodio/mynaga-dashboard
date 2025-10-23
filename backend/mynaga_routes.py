"""Real-time MyNaga API integration endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from mynaga_sync import MyNagaSyncService
from scheduler import sync_manager, init_scheduler, trigger_manual_sync
from mynaga_link_service import get_mynaga_report_link
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/mynaga", tags=["MyNaga Integration"])


class MyNagaConfig(BaseModel):
    """MyNaga configuration."""
    auth_token: str
    sync_interval_minutes: Optional[int] = 5


class SyncStatus(BaseModel):
    """Sync status response."""
    last_sync_time: Optional[str]
    last_sync_status: Optional[dict]
    is_syncing: bool


@router.post("/config")
def set_mynaga_config(config: MyNagaConfig, db: Session = Depends(get_db)):
    """
    Configure MyNaga API integration.
    
    Args:
        config: MyNaga configuration with auth token
        db: Database session
        
    Returns:
        Success message
    """
    try:
        # Initialize scheduler with the token
        init_scheduler(config.auth_token, config.sync_interval_minutes)
        
        return {
            "success": True,
            "message": "MyNaga integration configured",
            "sync_interval": config.sync_interval_minutes
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sync/manual")
async def manual_sync(auth_token: str, db: Session = Depends(get_db)):
    """
    Manually trigger MyNaga data sync.
    
    Args:
        auth_token: MyNaga authentication token
        db: Database session
        
    Returns:
        Sync statistics
    """
    try:
        stats = await trigger_manual_sync(auth_token)
        return {
            "success": True,
            "stats": stats
        }
    
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid auth token")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail="Token lacks permissions")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sync/status", response_model=SyncStatus)
def get_sync_status():
    """
    Get current MyNaga sync status.
    
    Returns:
        Sync status information
    """
    status = sync_manager.get_sync_status()
    return {
        "last_sync_time": status["last_sync_time"].isoformat() if status["last_sync_time"] else None,
        "last_sync_status": status["last_sync_status"],
        "is_syncing": status["is_syncing"]
    }


@router.post("/test-connection")
async def test_mynaga_connection(auth_token: str):
    """
    Test connection to MyNaga API.
    
    Args:
        auth_token: MyNaga authentication token
        
    Returns:
        Connection test result
    """
    try:
        from mynaga_sync import MyNagaAPIClient
        from datetime import datetime, timedelta
        
        async with MyNagaAPIClient(auth_token) as client:
            # Fetch reports from last 7 days to test connection
            date_from = datetime.utcnow() - timedelta(days=7)
            data = await client.fetch_reports(date_from=date_from)
            
            return {
                "success": True,
                "message": "Connection successful",
                "sample_count": len(data) if isinstance(data, list) else 0
            }
    
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Token lacks required permissions")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")


@router.post("/sync/stop")
def stop_sync():
    """Stop the automatic sync scheduler."""
    try:
        from scheduler import stop_scheduler
        stop_scheduler()
        
        return {
            "success": True,
            "message": "Sync scheduler stopped"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report-link/{control_no}")
async def get_report_link(control_no: str):
    """
    Get MyNaga report link for a specific control number.
    
    Args:
        control_no: The control number (e.g., "OTH-251022-2523")
        
    Returns:
        MyNaga report URL
    """
    try:
        link = await get_mynaga_report_link(control_no)
        
        if link:
            return {
                "success": True,
                "control_no": control_no,
                "link": link
            }
        else:
            return {
                "success": False,
                "control_no": control_no,
                "link": None,
                "message": "Report not found in MyNaga API"
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching report link: {str(e)}")
