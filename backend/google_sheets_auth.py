"""
Google Sheets Authentication Handler for Private Sheets
Supports both public CSV URLs and private sheets via Service Account
"""
import json
import os
from typing import Optional, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleSheetsAuthenticator:
    """
    Handles authentication to Google Sheets API
    Supports private sheets using Service Account credentials
    """
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Read and write access
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize with optional service account credentials
        
        Args:
            credentials_path: Path to service account JSON file
        """
        self.credentials_path = credentials_path or os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        self.credentials = None
        self.service = None
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            self._load_credentials()
    
    def _load_credentials(self):
        """Load service account credentials from JSON file"""
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            self.service = build('sheets', 'v4', credentials=self.credentials)
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")
            self.credentials = None
            self.service = None
    
    def set_credentials_from_json(self, credentials_json: str):
        """
        Set credentials from JSON string (for storing in database)
        
        Args:
            credentials_json: Service account credentials as JSON string
        """
        try:
            credentials_info = json.loads(credentials_json)
            self.credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=self.SCOPES
            )
            self.service = build('sheets', 'v4', credentials=self.credentials)
            return True
        except Exception as e:
            print(f"Error setting credentials from JSON: {str(e)}")
            return False
    
    def read_sheet(self, spreadsheet_id: str, range_name: str = None, gid: int = None) -> Optional[Dict[str, Any]]:
        """
        Read data from a private Google Sheet
        
        Args:
            spreadsheet_id: The ID of the spreadsheet (from URL)
            range_name: The A1 notation of the range to retrieve (optional, will auto-detect)
            gid: The sheet ID (gid parameter from URL) - if provided, will find sheet name
        
        Returns:
            Dictionary with sheet data or None if error
        """
        if not self.service:
            raise ValueError("Google Sheets service not initialized. Please provide credentials.")
        
        try:
            # If gid is provided, get the sheet name from it
            if gid is not None and not range_name:
                range_name = self.get_sheet_name_by_gid(spreadsheet_id, gid)
                if range_name:
                    print(f"Found sheet name '{range_name}' for gid={gid}")
            
            # If no range specified, try to find "Main" sheet first, then fall back to first sheet
            if not range_name:
                metadata = self.get_sheet_metadata(spreadsheet_id)
                if metadata and metadata.get('sheets'):
                    # Try to find "Main" sheet first
                    for sheet in metadata['sheets']:
                        properties = sheet.get('properties', {})
                        title = properties.get('title', '')
                        if title.lower() == 'main':
                            range_name = title
                            print(f"Found 'Main' sheet, using it")
                            break
                    
                    # If no "Main" sheet, use the first sheet
                    if not range_name:
                        first_sheet = metadata['sheets'][0]
                        if 'properties' in first_sheet:
                            range_name = first_sheet['properties']['title']
                        elif 'title' in first_sheet:
                            range_name = first_sheet['title']
                        else:
                            range_name = 'Sheet1'
                else:
                    range_name = 'Sheet1'  # Fallback
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            return {
                'values': result.get('values', []),
                'range': result.get('range', ''),
                'majorDimension': result.get('majorDimension', 'ROWS')
            }
        except HttpError as error:
            print(f"An error occurred: {error}")
            if error.resp.status == 403:
                raise PermissionError(
                    "Access denied. Make sure the service account email has access to the sheet."
                )
            elif error.resp.status == 404:
                raise FileNotFoundError("Spreadsheet not found. Check the spreadsheet ID.")
            elif error.resp.status == 400:
                # Try to get the actual sheet name and retry
                try:
                    metadata = self.get_sheet_metadata(spreadsheet_id)
                    if metadata and metadata.get('sheets'):
                        actual_sheet_name = metadata['sheets'][0]['title']
                        result = self.service.spreadsheets().values().get(
                            spreadsheetId=spreadsheet_id,
                            range=actual_sheet_name
                        ).execute()
                        return {
                            'values': result.get('values', []),
                            'range': result.get('range', ''),
                            'majorDimension': result.get('majorDimension', 'ROWS')
                        }
                except:
                    pass
                raise ValueError(f"Unable to parse range. Make sure the sheet exists. Error: {error}")
            raise
    
    def write_to_sheet(self, spreadsheet_id: str, range_name: str, values: list) -> bool:
        """
        Write data back to a Google Sheet
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
            range_name: The A1 notation of the range to update (e.g., "Main!A2:Z2")
            values: List of lists containing the data to write
        
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            raise ValueError("Google Sheets service not initialized. Please provide credentials.")
        
        try:
            body = {
                'values': values
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',  # Parses input as if entered in UI
                body=body
            ).execute()
            
            updated_cells = result.get('updatedCells', 0)
            print(f"Successfully updated {updated_cells} cells in range {range_name}")
            return True
            
        except HttpError as error:
            print(f"Error writing to sheet: {error}")
            if error.resp.status == 403:
                raise PermissionError(
                    "Access denied. Make sure the service account has EDITOR access to the sheet."
                )
            return False
    
    def find_row_by_control_no(self, spreadsheet_id: str, sheet_name: str, control_no: str) -> Optional[int]:
        """
        Find the row number for a specific control number
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
            sheet_name: Name of the sheet (e.g., "Main")
            control_no: The control number to search for (Column A)
        
        Returns:
            Row number (1-indexed) or None if not found
        """
        try:
            # Read all data from the sheet
            result = self.read_sheet(spreadsheet_id, sheet_name)
            if not result or 'values' not in result:
                return None
            
            values = result['values']
            
            # Search for control_no in first column (Column A)
            for row_idx, row in enumerate(values):
                if row and len(row) > 0:
                    # Row index is 0-based, but sheet rows are 1-indexed
                    if str(row[0]).strip() == str(control_no).strip():
                        return row_idx + 1  # Return 1-indexed row number
            
            return None
            
        except Exception as e:
            print(f"Error finding row by control_no: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if service account credentials are loaded"""
        return self.credentials is not None and self.service is not None
    
    @staticmethod
    def extract_spreadsheet_id(url: str) -> Optional[str]:
        """
        Extract spreadsheet ID from Google Sheets URL
        
        Args:
            url: Full Google Sheets URL
        
        Returns:
            Spreadsheet ID or None
        """
        import re
        
        # Pattern for Google Sheets URLs
        # https://docs.google.com/spreadsheets/d/{ID}/edit...
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)
        
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def extract_gid(url: str) -> Optional[int]:
        """
        Extract gid (sheet ID) from Google Sheets URL
        
        Args:
            url: Full Google Sheets URL with gid parameter
        
        Returns:
            Sheet gid as integer or None
        """
        import re
        
        # Pattern for gid in URLs
        # ...gid=123456...
        pattern = r'[?&#]gid=(\d+)'
        match = re.search(pattern, url)
        
        if match:
            return int(match.group(1))
        return None
    
    def get_sheet_name_by_gid(self, spreadsheet_id: str, gid: int) -> Optional[str]:
        """
        Get sheet name from gid
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
            gid: The sheet ID (gid)
        
        Returns:
            Sheet name or None
        """
        try:
            metadata = self.get_sheet_metadata(spreadsheet_id)
            if metadata and 'sheets' in metadata:
                for sheet in metadata['sheets']:
                    properties = sheet.get('properties', {})
                    if properties.get('sheetId') == gid:
                        return properties.get('title')
            return None
        except Exception as e:
            print(f"Error getting sheet name by gid: {e}")
            return None
    
    def get_sheet_metadata(self, spreadsheet_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata about the spreadsheet (title, sheets, etc.)
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
        
        Returns:
            Dictionary with metadata or None
        """
        if not self.service:
            raise ValueError("Google Sheets service not initialized")
        
        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            return {
                'title': result.get('properties', {}).get('title', ''),
                'sheets': [
                    {
                        'properties': {
                            'title': sheet['properties']['title'],
                            'sheetId': sheet['properties']['sheetId'],
                            'index': sheet['properties']['index']
                        }
                    }
                    for sheet in result.get('sheets', [])
                ]
            }
        except HttpError as error:
            print(f"Error getting metadata: {error}")
            return None


# Service account setup instructions
SETUP_INSTRUCTIONS = """
=== HOW TO SET UP GOOGLE SHEETS SERVICE ACCOUNT (FOR PRIVATE SHEETS) ===

1. Go to Google Cloud Console: https://console.cloud.google.com

2. Create a New Project (or select existing):
   - Click "Select a project" → "New Project"
   - Give it a name (e.g., "MyNaga Dashboard")
   - Click "Create"

3. Enable Google Sheets API:
   - Search for "Google Sheets API" in the search bar
   - Click "Enable"

4. Create Service Account:
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "mynaga-sync")
   - Click "Create and Continue"
   - Skip role selection (click "Continue")
   - Click "Done"

5. Generate Key File:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Click "Create"
   - A JSON file will download - SAVE THIS FILE SECURELY!

6. Share Your Google Sheet:
   - Open your Google Sheet
   - Click "Share" button
   - Copy the service account email (looks like: xxx@xxx.iam.gserviceaccount.com)
   - Paste it in the "Add people and groups" field
   - Set permission to "Viewer"
   - Uncheck "Notify people"
   - Click "Share"

7. Upload Credentials in Dashboard:
   - Go to Google Sheets Setup page
   - Click "Upload Service Account Key"
   - Select the downloaded JSON file
   - OR paste the JSON content directly

That's it! You can now sync private Google Sheets.
"""
