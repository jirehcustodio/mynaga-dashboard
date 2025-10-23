"""Background task scheduler for real-time MyNaga and Google Sheets data sync."""
import asyncio
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from database import SessionLocal
from mynaga_sync import sync_mynaga_data
from google_sheets_sync import GoogleSheetsSync
from typing import Optional

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler: BackgroundScheduler = None
sync_task_id = "mynaga_sync_task"
sheets_sync_task_id = "google_sheets_sync_task"


class SyncManager:
    """Manages background sync tasks."""
    
    def __init__(self):
        """Initialize sync manager."""
        self.last_sync_time: datetime = None
        self.last_sync_status: dict = None
        self.is_syncing = False
        
        # Google Sheets sync tracking
        self.sheets_last_sync_time: datetime = None
        self.sheets_last_sync_status: dict = None
        self.sheets_is_syncing = False
        self.sheets_config: Optional[dict] = None
    
    async def run_sync(self, auth_token: str):
        """
        Run the sync task.
        
        Args:
            auth_token: MyNaga authentication token
        """
        if self.is_syncing:
            logger.warning("Sync already in progress, skipping...")
            return
        
        self.is_syncing = True
        try:
            logger.info("Starting MyNaga sync task...")
            db: Session = SessionLocal()
            
            stats = await sync_mynaga_data(auth_token, db)
            
            self.last_sync_time = datetime.utcnow()
            self.last_sync_status = stats
            
            logger.info(f"Sync completed: {stats}")
            
        except Exception as e:
            logger.error(f"Sync task failed: {e}")
            self.last_sync_status = {"error": str(e)}
        
        finally:
            self.is_syncing = False
            if 'db' in locals():
                db.close()
    
    async def run_google_sheets_sync(self):
        """Run Google Sheets sync task."""
        if self.sheets_is_syncing:
            logger.warning("Google Sheets sync already in progress, skipping...")
            return
        
        if not self.sheets_config:
            logger.warning("No Google Sheets configuration set, skipping sync")
            return
        
        self.sheets_is_syncing = True
        try:
            logger.info("Starting Google Sheets sync task...")
            db: Session = SessionLocal()
            
            sheets_sync = GoogleSheetsSync(
                sheet_url=self.sheets_config.get('sheet_url'),
                db=db,
                credentials_json=self.sheets_config.get('credentials_json')
            )
            
            stats = await sheets_sync.sync_to_database()
            
            self.sheets_last_sync_time = datetime.utcnow()
            self.sheets_last_sync_status = stats
            
            logger.info(f"Google Sheets sync completed: {stats}")
            
        except Exception as e:
            logger.error(f"Google Sheets sync task failed: {e}")
            self.sheets_last_sync_status = {"error": str(e)}
        
        finally:
            self.sheets_is_syncing = False
            if 'db' in locals():
                db.close()
    
    def set_sheets_config(self, sheet_url: str, credentials_json: Optional[str] = None):
        """Set Google Sheets configuration for automatic sync."""
        self.sheets_config = {
            'sheet_url': sheet_url,
            'credentials_json': credentials_json
        }
        logger.info(f"Google Sheets config updated: sheet_url={sheet_url}")
    
    def get_sync_status(self) -> dict:
        """Get current sync status."""
        return {
            "mynaga": {
                "last_sync_time": self.last_sync_time,
                "last_sync_status": self.last_sync_status,
                "is_syncing": self.is_syncing
            },
            "google_sheets": {
                "last_sync_time": self.sheets_last_sync_time,
                "last_sync_status": self.sheets_last_sync_status,
                "is_syncing": self.sheets_is_syncing,
                "configured": self.sheets_config is not None
            }
        }


# Global sync manager
sync_manager = SyncManager()


def init_scheduler(auth_token: str, sync_interval_minutes: int = 5):
    """
    Initialize background scheduler for MyNaga sync.
    
    Args:
        auth_token: MyNaga authentication token
        sync_interval_minutes: Interval between syncs in minutes
    """
    global scheduler
    
    try:
        if scheduler is None:
            scheduler = BackgroundScheduler()
            scheduler.start()
            logger.info("Scheduler started")
        
        # Add sync job
        def sync_job():
            """Wrapper for sync task."""
            asyncio.run(sync_manager.run_sync(auth_token))
        
        # Remove existing job if present
        try:
            scheduler.remove_job(sync_task_id)
        except:
            pass
        
        # Add new job
        scheduler.add_job(
            sync_job,
            IntervalTrigger(minutes=sync_interval_minutes),
            id=sync_task_id,
            name="MyNaga Data Sync",
            replace_existing=True
        )
        
        logger.info(
            f"MyNaga sync scheduled: Every {sync_interval_minutes} minutes"
        )
        
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}")


def stop_scheduler():
    """Stop the background scheduler."""
    global scheduler
    
    if scheduler and scheduler.running:
        scheduler.shutdown()
        scheduler = None
        logger.info("Scheduler stopped")


async def trigger_manual_sync(auth_token: str):
    """
    Manually trigger a sync immediately.
    
    Args:
        auth_token: MyNaga authentication token
        
    Returns:
        Sync statistics
    """
    await sync_manager.run_sync(auth_token)
    return sync_manager.last_sync_status


def init_google_sheets_scheduler(sheet_url: str, credentials_json: Optional[str] = None, sync_interval_seconds: int = 10):
    """
    Initialize background scheduler for Google Sheets sync.
    
    Args:
        sheet_url: Google Sheets URL (full URL with gid)
        credentials_json: Optional service account credentials JSON
        sync_interval_seconds: Interval between syncs in seconds (default: 10)
    """
    global scheduler
    
    try:
        # Set configuration
        sync_manager.set_sheets_config(sheet_url, credentials_json)
        
        if scheduler is None:
            scheduler = BackgroundScheduler()
            scheduler.start()
            logger.info("Scheduler started")
        
        # Add sync job
        def sync_job():
            """Wrapper for Google Sheets sync task."""
            asyncio.run(sync_manager.run_google_sheets_sync())
        
        # Remove existing job if present
        try:
            scheduler.remove_job(sheets_sync_task_id)
        except:
            pass
        
        # Add new job
        scheduler.add_job(
            sync_job,
            IntervalTrigger(seconds=sync_interval_seconds),
            id=sheets_sync_task_id,
            name="Google Sheets Data Sync",
            replace_existing=True
        )
        
        logger.info(
            f"Google Sheets sync scheduled: Every {sync_interval_seconds} seconds"
        )
        
        return {"message": f"Auto-sync enabled: every {sync_interval_seconds} seconds"}
        
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets scheduler: {e}")
        return {"error": str(e)}


def stop_google_sheets_scheduler():
    """Stop Google Sheets automatic sync."""
    global scheduler
    
    if scheduler:
        try:
            scheduler.remove_job(sheets_sync_task_id)
            logger.info("Google Sheets sync stopped")
            return {"message": "Auto-sync stopped"}
        except:
            pass
    
    return {"message": "No active sync to stop"}


async def trigger_manual_sheets_sync():
    """
    Manually trigger Google Sheets sync immediately.
    
    Returns:
        Sync statistics
    """
    await sync_manager.run_google_sheets_sync()
    return sync_manager.sheets_last_sync_status
