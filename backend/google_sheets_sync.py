"""Google Sheets synchronization for real-time data import."""
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
from sqlalchemy.orm import Session
from models import Case
from schemas import CaseCreate

logger = logging.getLogger(__name__)


class GoogleSheetsSync:
    """Sync data from Google Sheets."""
    
    def __init__(self, sheet_url: str, db: Session, credentials_json: Optional[str] = None):
        """
        Initialize Google Sheets sync.
        
        Args:
            sheet_url: Google Sheets URL (published as CSV or private sheet)
            db: Database session
            credentials_json: Optional service account credentials JSON string
        """
        self.sheet_url = sheet_url
        self.db = db
        self.credentials_json = credentials_json
        self.use_service_account = credentials_json is not None
        
        # Extract sheet ID and gid from URL
        self.sheet_id = self._extract_sheet_id(sheet_url)
        self.gid = self._extract_gid(sheet_url)
        
        if not self.use_service_account:
            # Convert to CSV export URL if it's a regular sheet URL
            if '/edit' in sheet_url or '/view' in sheet_url:
                if self.sheet_id:
                    # Try export URL first
                    self.csv_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv"
                else:
                    self.csv_url = sheet_url
            else:
                self.csv_url = sheet_url
    
    def _extract_sheet_id(self, url: str) -> Optional[str]:
        """Extract spreadsheet ID from URL."""
        import re
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None
    
    def _extract_gid(self, url: str) -> Optional[int]:
        """Extract gid (sheet ID) from URL."""
        import re
        pattern = r'[?&#]gid=(\d+)'
        match = re.search(pattern, url)
        return int(match.group(1)) if match else None
    
    async def fetch_sheet_data(self) -> List[Dict[str, Any]]:
        """
        Fetch data from Google Sheets (via CSV or API).
        
        Returns:
            List of row dictionaries
        """
        if self.use_service_account:
            return await self._fetch_via_api()
        else:
            return await self._fetch_via_csv()
    
    async def _fetch_via_csv(self) -> List[Dict[str, Any]]:
        """Fetch data via published CSV URL."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.csv_url) as response:
                    if response.status == 200:
                        csv_data = await response.text()
                        return self._parse_csv(csv_data)
                    elif response.status == 403:
                        raise Exception(
                            "Access denied. Please publish your sheet as CSV: "
                            "File → Share → Publish to web → CSV format"
                        )
                    else:
                        raise Exception(f"Failed to fetch sheet: {response.status}")
        except Exception as e:
            logger.error(f"Error fetching Google Sheet: {str(e)}")
            raise
    
    async def _fetch_via_api(self) -> List[Dict[str, Any]]:
        """Fetch data via Google Sheets API (private sheets)."""
        try:
            from google_sheets_auth import GoogleSheetsAuthenticator
            
            auth = GoogleSheetsAuthenticator()
            
            # Set credentials from JSON string
            if not auth.set_credentials_from_json(self.credentials_json):
                raise Exception("Invalid service account credentials")
            
            # Fetch sheet data - pass gid if available to read the correct tab
            logger.info(f"Fetching from sheet ID: {self.sheet_id}, gid: {self.gid}")
            result = auth.read_sheet(self.sheet_id, range_name=None, gid=self.gid)
            
            if not result or not result.get('values'):
                return []
            
            # Convert to list of dictionaries
            values = result['values']
            if len(values) < 2:
                return []
            
            headers = values[0]
            logger.info(f"Found {len(headers)} columns: {', '.join(headers[:5])}...")
            
            rows = []
            
            for row_values in values[1:]:
                # Pad row with empty strings if shorter than headers
                padded_row = row_values + [''] * (len(headers) - len(row_values))
                row_dict = dict(zip(headers, padded_row))
                rows.append(row_dict)
            
            logger.info(f"Successfully parsed {len(rows)} rows")
            return rows
            
        except PermissionError as e:
            logger.error(f"Permission denied: {str(e)}")
            raise Exception(f"Permission denied. Make sure you shared the sheet with: {auth.credentials.service_account_email if hasattr(auth.credentials, 'service_account_email') else 'the service account email'}")
        except FileNotFoundError as e:
            logger.error(f"Spreadsheet not found: {str(e)}")
            raise Exception("Spreadsheet not found. Please check the URL.")
        except Exception as e:
            logger.error(f"Error fetching via API: {str(e)}")
            raise
    
    def _parse_csv(self, csv_data: str) -> List[Dict[str, Any]]:
        """
        Parse CSV data into list of dictionaries.
        
        Args:
            csv_data: CSV string data
            
        Returns:
            List of row dictionaries
        """
        import csv
        from io import StringIO
        
        rows = []
        csv_reader = csv.DictReader(StringIO(csv_data))
        
        for row in csv_reader:
            # Clean up row data
            cleaned_row = {k.strip(): v.strip() if v else None for k, v in row.items()}
            rows.append(cleaned_row)
        
        return rows
    
    def _map_row_to_case(self, row: Dict[str, Any]) -> Optional[CaseCreate]:
        """
        Map a spreadsheet row to a Case object.
        
        Args:
            row: Row data from spreadsheet
            
        Returns:
            CaseCreate object or None if invalid
        """
        # Flexible column mapping
        column_mappings = {
            'control_no': ['Control No.', 'Control No', 'ID', 'Case ID', 'Control Number'],
            'category': ['Category', 'Type', 'Issue Type'],
            'sender_location': ['Sender\'s Location', 'Location', 'Address'],
            'cluster': ['Cluster', 'Cluster Group', 'Group'],  # Column D
            'barangay': ['Barangay', 'Brgy'],
            'description': ['Description', 'Details'],
            'attached_media': ['Attached Media', 'Media', 'Attachments', 'Image/Video'],  # Media URLs
            'date_created': ['Date Created', 'Date', 'Created At'],
            'reported_by': ['Reported by', 'Reporter', 'Name'],
            'contact_number': ['Contact Number', 'Contact', 'Phone'],
            'office': ['Office', 'Office Code', 'Assigned Office'],  # Column I
            'link_to_report': ['Link to Report', 'Link', 'URL'],
            'mynaga_app_status': ['MyNaga App Status', 'App Status', 'MyNaga Status'],  # Column M
            'updates_sent_to_user_new': ['Updates Sent to User', 'Auto Response', 'Message'],  # Column N
            'status': ['OPEN/RESOLVED/FOR REROUTING', 'Status', 'Case Status'],
        }
        
        # Extract data using flexible mapping
        case_data = {}
        
        for field, possible_columns in column_mappings.items():
            for col_name in possible_columns:
                if col_name in row and row[col_name]:
                    case_data[field] = row[col_name]
                    break
        
        # Control number is required
        if 'control_no' not in case_data:
            return None
        
        # Set defaults for missing required fields
        case_data.setdefault('category', 'Uncategorized')
        case_data.setdefault('sender_location', 'Unknown')
        case_data.setdefault('barangay', 'Unknown')
        case_data.setdefault('description', 'No description provided')
        
        # Normalize status values to match dashboard expectations
        if 'status' in case_data:
            status_value = str(case_data['status']).strip().lower()
            
            # Map various status values to the three main categories
            status_mapping = {
                # OPEN variations
                'open': 'OPEN',
                'in progress': 'OPEN',
                'pending': 'OPEN',
                'pending confirmation': 'OPEN',
                'no status yet': 'OPEN',
                'new': 'OPEN',
                'active': 'OPEN',
                
                # RESOLVED variations
                'resolved': 'RESOLVED',
                'completed': 'RESOLVED',
                'closed': 'RESOLVED',
                'done': 'RESOLVED',
                'fixed': 'RESOLVED',
                
                # FOR REROUTING variations
                'for rerouting': 'FOR REROUTING',
                'rerouting': 'FOR REROUTING',
                'reroute': 'FOR REROUTING',
                'transferred': 'FOR REROUTING',
                'forwarded': 'FOR REROUTING',
            }
            
            # Apply mapping or default to OPEN
            case_data['status'] = status_mapping.get(status_value, 'OPEN')
        else:
            # Default status if not provided
            case_data['status'] = 'OPEN'
        
        # Parse date if present
        if 'date_created' in case_data and isinstance(case_data['date_created'], str):
            try:
                case_data['date_created'] = datetime.fromisoformat(case_data['date_created'].replace('/', '-'))
            except:
                try:
                    from dateutil import parser
                    case_data['date_created'] = parser.parse(case_data['date_created'])
                except:
                    case_data['date_created'] = datetime.utcnow()
        
        try:
            return CaseCreate(**case_data)
        except Exception as e:
            logger.error(f"Error creating case from row: {str(e)}")
            return None
    
    async def sync_to_database(self) -> Dict[str, Any]:
        """
        Sync Google Sheets data to database.
        
        Returns:
            Sync statistics
        """
        stats = {
            'fetched': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }
        
        try:
            # Fetch data from sheet
            rows = await self.fetch_sheet_data()
            stats['fetched'] = len(rows)
            
            # Process each row
            for idx, row in enumerate(rows):
                try:
                    case_data = self._map_row_to_case(row)
                    
                    if not case_data:
                        stats['skipped'] += 1
                        continue
                    
                    # Check if case already exists
                    existing = self.db.query(Case).filter(
                        Case.control_no == case_data.control_no
                    ).first()
                    
                    if existing:
                        # Update existing case
                        for key, value in case_data.dict().items():
                            if value is not None:
                                setattr(existing, key, value)
                        existing.updated_at = datetime.utcnow()
                        stats['updated'] += 1
                    else:
                        # Create new case
                        new_case = Case(**case_data.dict())
                        self.db.add(new_case)
                        stats['created'] += 1
                
                except Exception as e:
                    error_msg = f"Row {idx + 2}: {str(e)}"
                    stats['errors'].append(error_msg)
                    logger.error(error_msg)
            
            # Commit all changes
            self.db.commit()
            
            return stats
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Sync failed: {str(e)}")


async def sync_from_google_sheets(sheet_url: str, db: Session) -> Dict[str, Any]:
    """
    Synchronize data from Google Sheets.
    
    Args:
        sheet_url: Google Sheets URL
        db: Database session
        
    Returns:
        Sync statistics
    """
    syncer = GoogleSheetsSync(sheet_url, db)
    return await syncer.sync_to_database()


def write_case_to_sheet(
    case_data: Dict[str, Any],
    sheet_url: str,
    credentials_json: str
) -> bool:
    """
    Write updated case data back to Google Sheets.
    
    Args:
        case_data: Dictionary containing case data with control_no
        sheet_url: Google Sheets URL
        credentials_json: Service account credentials JSON string
        
    Returns:
        True if successful, False otherwise
    """
    from google_sheets_auth import GoogleSheetsAuthenticator
    import re
    
    try:
        # Extract spreadsheet ID and gid
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, sheet_url)
        if not match:
            logger.error("Invalid sheet URL")
            return False
        
        spreadsheet_id = match.group(1)
        
        # Extract gid
        gid_pattern = r'[?&#]gid=(\d+)'
        gid_match = re.search(gid_pattern, sheet_url)
        gid = int(gid_match.group(1)) if gid_match else None
        
        # Initialize authenticator
        auth = GoogleSheetsAuthenticator()
        if not auth.set_credentials_from_json(credentials_json):
            logger.error("Failed to set credentials")
            return False
        
        # Get sheet name from gid
        sheet_name = auth.get_sheet_name_by_gid(spreadsheet_id, gid) if gid else "Main"
        if not sheet_name:
            sheet_name = "Main"
        
        logger.info(f"Writing to sheet: {sheet_name}")
        
        # Find row by control number
        control_no = case_data.get('control_no')
        if not control_no:
            logger.error("No control_no in case data")
            return False
        
        row_number = auth.find_row_by_control_no(spreadsheet_id, sheet_name, control_no)
        if not row_number:
            logger.error(f"Case {control_no} not found in sheet")
            return False
        
        logger.info(f"Found case {control_no} at row {row_number}")
        
        # Map case data to sheet columns based on actual spreadsheet structure
        # Column order from the spreadsheet (based on AppScript):
        # A: Control No.
        # B: (unknown/not mapped yet)
        # C: Category
        # D: Cluster
        # E-H: (other fields like Location, Barangay, Description, Date, Reported by, Contact)
        # I: Office
        # J-L: (other fields)
        # M: MyNaga App Status
        # N: Updates Sent to User (Auto-response message)
        # K or other: OPEN/RESOLVED/FOR REROUTING (Status)
        
        # For now, we'll update the key columns that are editable in your dashboard
        # We need to read the full row first to preserve other data
        
        # Read the entire row
        full_row_data = auth.read_sheet(spreadsheet_id, f"{sheet_name}!A{row_number}:Z{row_number}")
        if not full_row_data or 'values' not in full_row_data or not full_row_data['values']:
            logger.error(f"Could not read row {row_number}")
            return False
        
        existing_row = full_row_data['values'][0] if full_row_data['values'] else []
        
        # Ensure the row has enough columns (at least 14 for column N)
        while len(existing_row) < 14:
            existing_row.append('')
        
        # Update only the specific columns we want to sync
        # Column D (index 3): Cluster
        existing_row[3] = case_data.get('cluster', existing_row[3] if len(existing_row) > 3 else '')
        
        # Column I (index 8): Office
        existing_row[8] = case_data.get('office', existing_row[8] if len(existing_row) > 8 else '')
        
        # Column M (index 12): MyNaga App Status
        existing_row[12] = case_data.get('mynaga_app_status', existing_row[12] if len(existing_row) > 12 else '')
        
        # Column N (index 13): Updates Sent to User (auto-response)
        # Only update if explicitly provided, otherwise keep existing
        if 'updates_sent_to_user' in case_data and case_data['updates_sent_to_user']:
            existing_row[13] = case_data.get('updates_sent_to_user', '')
        elif 'updates_sent_to_user_new' in case_data and case_data['updates_sent_to_user_new']:
            existing_row[13] = case_data.get('updates_sent_to_user_new', '')
        
        # Update the row in the sheet (A to N)
        range_name = f"{sheet_name}!A{row_number}:N{row_number}"
        success = auth.write_to_sheet(spreadsheet_id, range_name, [existing_row[:14]])
        
        if success:
            logger.info(f"Successfully wrote case {control_no} to Google Sheets")
        else:
            logger.error(f"Failed to write case {control_no} to Google Sheets")
        
        return success
        
    except Exception as e:
        logger.error(f"Error writing to sheet: {str(e)}")
        return False
