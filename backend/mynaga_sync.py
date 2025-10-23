"""MyNaga API integration for real-time data syncing."""
import aiohttp
import asyncio
import ssl
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging
from sqlalchemy.orm import Session
from models import Case, Office
from schemas import CaseCreate

logger = logging.getLogger(__name__)


class MyNagaAPIClient:
    """Client for MyNaga App API real-time data sync."""
    
    # MyNaga API endpoints
    BASE_URL = "https://mynaga.app/api"
    REPORTS_ENDPOINT = f"{BASE_URL}/reports"
    
    def __init__(self, auth_token: str):
        """
        Initialize MyNaga API client.
        
        Args:
            auth_token: Authentication token from MyNaga App
        """
        self.auth_token = auth_token
        # MyNaga API expects the token directly, not "Bearer {token}"
        self.headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        # Create SSL context that handles certificates properly
        ssl_context = ssl.create_default_context()
        # For development: you can uncomment the line below if you have SSL issues
        # ssl_context.check_hostname = False
        # ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def fetch_reports(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch reports from MyNaga API.
        
        Args:
            date_from: Start date for filtering (optional)
            date_to: End date for filtering (optional)
            
        Returns:
            List of report dictionaries
        """
        if not self.session:
            await self._initialize_session()
        
        # Build query parameters to match AppScript implementation
        params = {
            "filter_cancel": "1"  # Filter out cancelled reports
        }
        
        if date_from:
            params["date_created_from"] = date_from.strftime("%Y-%m-%d")
        if date_to:
            params["date_created_to"] = date_to.strftime("%Y-%m-%d")
        
        try:
            # Use /reports endpoint directly (AppScript shows BASE_API_URL includes /reports)
            url = f"{self.BASE_URL}/reports"
            logger.info(f"Fetching reports from: {url} with params: {params}")
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # API returns array of report objects
                    logger.info(f"Successfully fetched {len(data)} reports")
                    return data
                else:
                    error_text = await response.text()
                    logger.error(f"API request failed with status {response.status}: {error_text}")
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Error fetching reports: {str(e)}")
            raise


class MyNagaSyncService:
    """Service to sync MyNaga data to local database."""
    
    def __init__(self, auth_token: str, db: Session):
        """
        Initialize sync service.
        
        Args:
            auth_token: MyNaga authentication token
            db: Database session
        """
        self.client = MyNagaAPIClient(auth_token)
        self.db = db
    
    def _map_mynaga_to_case(self, mynaga_report: Dict) -> CaseCreate:
        """
        Map MyNaga report to Case model (matching AppScript structure).
        
        Args:
            mynaga_report: Report data from MyNaga API
            
        Returns:
            CaseCreate schema instance
        """
        # Extract user info
        user = mynaga_report.get("user", {})
        user_name = user.get("name", "")
        user_mobile = user.get("mobile", "")
        
        # Extract cluster status
        cluster = mynaga_report.get("report_cluster", {})
        cluster_status = cluster.get("status", "")
        
        # Extract offices (can be array or single object)
        offices = mynaga_report.get("offices", [])
        if isinstance(offices, dict):
            offices = [offices]
        office_names = ", ".join([o.get("name", "") for o in offices if isinstance(o, dict)])
        
        # Extract images
        images = mynaga_report.get("images", [])
        image_urls = [img.get("url", "") for img in images if isinstance(img, dict) and img.get("url")]
        attached_media = ",".join(image_urls) if image_urls else None
        
        return CaseCreate(
            control_no=mynaga_report.get("control_number", ""),
            date_created=datetime.fromisoformat(
                mynaga_report.get("date_created", datetime.utcnow().isoformat())
            ),
            category=mynaga_report.get("report_type", {}).get("name", ""),
            sender_location=mynaga_report.get("location", ""),
            barangay=mynaga_report.get("barangay", {}).get("name", ""),
            description=mynaga_report.get("description", ""),
            attached_media=attached_media,
            reported_by=user_name,
            contact_number=user_mobile,
            link_to_report=f"https://mynaga.app/reports/{mynaga_report.get('_id', '')}",
            mynaga_app_status=cluster_status,
            refined_category=mynaga_report.get("refinedCategory"),
            status=self._map_status(cluster_status)
        )
    
    @staticmethod
    def _map_status(mynaga_status: str) -> str:
        """
        Map MyNaga status to local status.
        
        Args:
            mynaga_status: Status from MyNaga
            
        Returns:
            Local status (OPEN/RESOLVED/FOR REROUTING)
        """
        status_map = {
            "new": "OPEN",
            "open": "OPEN",
            "pending": "OPEN",
            "in_progress": "OPEN",
            "resolved": "RESOLVED",
            "closed": "RESOLVED",
            "for_rerouting": "FOR REROUTING",
            "reroute": "FOR REROUTING",
        }
        return status_map.get(mynaga_status.lower(), "OPEN")
    
    async def sync_reports(self) -> Dict:
        """
        Sync reports from MyNaga API to database.
        
        Returns:
            Dictionary with sync statistics
        """
        stats = {
            "total_fetched": 0,
            "created": 0,
            "updated": 0,
            "errors": 0,
            "error_messages": []
        }
        
        try:
            async with self.client as client:
                logger.info("Starting MyNaga sync...")
                # Fetch reports from last 30 days by default
                date_from = datetime.utcnow().replace(day=1)  # First day of current month
                reports = await client.fetch_reports(date_from=date_from)
                stats["total_fetched"] = len(reports)
                
                for report in reports:
                    try:
                        # Check if case already exists
                        existing_case = self.db.query(Case).filter(
                            Case.control_no == report.get("id")
                        ).first()
                        
                        # Map to case
                        case_data = self._map_mynaga_to_case(report)
                        
                        if existing_case:
                            # Update existing case
                            for key, value in case_data.dict().items():
                                if value is not None:
                                    setattr(existing_case, key, value)
                            existing_case.updated_at = datetime.utcnow()
                            stats["updated"] += 1
                        else:
                            # Create new case
                            new_case = Case(**case_data.dict())
                            self.db.add(new_case)
                            stats["created"] += 1
                        
                    except Exception as e:
                        logger.error(f"Error processing report {report.get('id')}: {e}")
                        stats["errors"] += 1
                        stats["error_messages"].append(str(e))
                
                # Commit all changes
                self.db.commit()
                logger.info(f"Sync complete: {stats['created']} created, {stats['updated']} updated")
                
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            stats["errors"] += 1
            stats["error_messages"].append(str(e))
            self.db.rollback()
        
        return stats


async def sync_mynaga_data(auth_token: str, db: Session) -> Dict:
    """
    Perform MyNaga data sync.
    
    Args:
        auth_token: MyNaga authentication token
        db: Database session
        
    Returns:
        Sync statistics
    """
    service = MyNagaSyncService(auth_token, db)
    return await service.sync_reports()
