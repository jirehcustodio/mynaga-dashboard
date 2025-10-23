"""Excel file import functionality."""
import pandas as pd
from datetime import datetime
from typing import List, Tuple
from models import Case, Office
from sqlalchemy.orm import Session


class ExcelImporter:
    """Handle Excel file imports."""
    
    # Map various possible column names to our database fields
    COLUMN_MAPPINGS = {
        'control_no': [
            'Control No.', 'Control No', 'Control Number', 'control_no', 
            'ControlNo', 'ID', 'Case ID', 'Case No'
        ],
        'category': [
            'Category', 'category', 'Type', 'Report Type', 'Issue Type'
        ],
        'sender_location': [
            'Sender\'s Location', 'Sender Location', 'Location', 'sender_location',
            'Sender\'s Location', 'Reporter Location', 'Address'
        ],
        'barangay': [
            'Barangay', 'barangay', 'Brgy', 'Barangay/District'
        ],
        'description': [
            'Description', 'description', 'Details', 'Issue Description', 
            'Report Description', 'Message'
        ],
        'date_created': [
            'Date Created', 'Date', 'Created Date', 'date_created',
            'Timestamp', 'Created At', 'Report Date'
        ],
        'attached_media': [
            'Attached Media', 'Media', 'Images', 'Attachments', 'attached_media'
        ],
        'reported_by': [
            'Reported by', 'Reported By', 'Reporter', 'reported_by',
            'Name', 'User', 'Submitted By'
        ],
        'contact_number': [
            'Contact Number', 'Contact', 'Phone', 'Mobile', 'contact_number',
            'Phone Number', 'Mobile Number'
        ],
        'link_to_report': [
            'Link to Report', 'Link', 'URL', 'Report Link', 'link_to_report'
        ],
        'mynaga_app_status': [
            'MyNaga App Status', 'App Status', 'mynaga_app_status', 'MyNaga Status'
        ],
        'status': [
            'OPEN/RESOLVED/FOR REROUTING', 'Status', 'status', 'Case Status'
        ],
        'refined_category': [
            'Refined Category', 'refined_category', 'Sub Category', 'Subcategory'
        ],
    }

    @staticmethod
    def find_column_name(df: pd.DataFrame, field_name: str) -> str:
        """
        Find the actual column name in the DataFrame for a given field.
        
        Args:
            df: DataFrame to search
            field_name: Our internal field name
            
        Returns:
            Actual column name in the DataFrame, or None if not found
        """
        possible_names = ExcelImporter.COLUMN_MAPPINGS.get(field_name, [])
        for col_name in possible_names:
            if col_name in df.columns:
                return col_name
        return None

    @staticmethod
    def import_excel(file_path: str, db: Session) -> Tuple[int, List[str]]:
        """
        Import cases from Excel file.
        
        Args:
            file_path: Path to Excel file
            db: Database session
            
        Returns:
            Tuple of (imported_count, error_messages)
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            imported_count = 0
            errors = []
            
            # Map column names once at the start
            column_map = {}
            required_fields = ['control_no', 'category', 'sender_location', 'barangay', 'description']
            
            # Find all available columns
            for field_name in ExcelImporter.COLUMN_MAPPINGS.keys():
                actual_col = ExcelImporter.find_column_name(df, field_name)
                if actual_col:
                    column_map[field_name] = actual_col
            
            # Check if we have all required fields
            missing_required = [f for f in required_fields if f not in column_map]
            if missing_required:
                # Be lenient - only control_no is truly required
                if 'control_no' not in column_map:
                    errors.append(f"Missing critical column for Control Number. Available columns: {', '.join(df.columns)}")
                    return 0, errors
            
            # Process each row
            for idx, row in df.iterrows():
                try:
                    # Extract case data using mapped columns
                    case_data = {}
                    
                    # Get control number (required)
                    control_col = column_map.get('control_no')
                    if control_col and pd.notna(row[control_col]):
                        case_data['control_no'] = str(row[control_col]).strip()
                    else:
                        errors.append(f"Row {idx + 2}: Missing Control No.")
                        continue
                    
                    # Get other fields with fallbacks
                    for field_name, excel_col in column_map.items():
                        if field_name == 'control_no':
                            continue  # Already processed
                        
                        if pd.notna(row[excel_col]):
                            value = row[excel_col]
                            
                            # Handle dates specially
                            if field_name == 'date_created':
                                if isinstance(value, datetime):
                                    case_data[field_name] = value
                                else:
                                    try:
                                        case_data[field_name] = pd.to_datetime(value)
                                    except:
                                        pass  # Skip invalid dates
                            else:
                                # Convert to string and clean
                                case_data[field_name] = str(value).strip()
                    
                    # Set defaults for missing required fields
                    if 'category' not in case_data:
                        case_data['category'] = 'Uncategorized'
                    if 'sender_location' not in case_data:
                        case_data['sender_location'] = 'Unknown'
                    if 'barangay' not in case_data:
                        case_data['barangay'] = 'Unknown'
                    if 'description' not in case_data:
                        case_data['description'] = 'No description provided'
                    
                    # Check if case already exists
                    existing = db.query(Case).filter(
                        Case.control_no == case_data['control_no']
                    ).first()
                    
                    if existing:
                        # Update existing case
                        for key, value in case_data.items():
                            if hasattr(existing, key):
                                setattr(existing, key, value)
                        existing.updated_at = datetime.utcnow()
                    else:
                        # Create new case
                        case = Case(**case_data)
                        db.add(case)
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {idx + 2}: {str(e)}")
            
            # Commit all changes
            db.commit()
            
            return imported_count, errors
            
        except Exception as e:
            return 0, [f"Error reading Excel file: {str(e)}"]

    @staticmethod
    def export_cases(cases: List[Case], export_path: str) -> bool:
        """
        Export cases to Excel file.
        
        Args:
            cases: List of Case objects
            export_path: Path to export Excel file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert cases to dictionaries
            data = []
            for case in cases:
                data.append({
                    'Control No.': case.control_no,
                    'Date Created': case.date_created,
                    'Category': case.category,
                    'Cluster': ', '.join([c.name for c in case.clusters]),
                    'Sender\'s Location': case.sender_location,
                    'Barangay': case.barangay,
                    'Description': case.description,
                    'Attached Media': case.attached_media,
                    'Office': ', '.join([o.name for o in case.offices]),
                    'Reported by': case.reported_by,
                    'Contact Number': case.contact_number,
                    'Link to Report': case.link_to_report,
                    'MyNaga App Status': case.mynaga_app_status,
                    'Updates Sent to User': case.updates_sent_to_user,
                    'Status': case.status,
                    'Refined Category': case.refined_category,
                    'Case Aging': case.case_aging,
                    'Last Updated': case.updated_at,
                })
            
            # Create DataFrame and export
            df = pd.DataFrame(data)
            df.to_excel(export_path, index=False, sheet_name='Cases')
            
            return True
            
        except Exception as e:
            print(f"Error exporting cases: {str(e)}")
            return False
