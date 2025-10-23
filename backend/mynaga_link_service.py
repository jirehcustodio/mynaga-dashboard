"""
MyNaga Link Service
Fetches MongoDB ID from MyNaga API to generate report links
"""
import aiohttp
import ssl
import logging
from typing import Optional, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# MyNaga API Configuration
MYNAGA_API_BASE = "https://mynaga.app/api/reports"
# Updated token - expires Feb 2026
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OGE0ODk3Zjg1ZmIxYTdiYjU2YTNjYTQiLCJpYXQiOjE3NjA1ODE1NDgsImV4cCI6MTc2MTE4NjM0OH0.AlIem843s3R_SaGLQVMjP3EfYaVMrOKANoVYv7zX3ns"
FIXED_QUERY_PARAMS = "filter_cancel=1&sortQuery=%7B%22priority%22:-1,%22status%22:1,%22date_created%22:1%7D"


async def get_mynaga_report_id(control_no: str) -> Optional[str]:
    """
    Fetch MongoDB _id for a specific control number from MyNaga API.
    
    Args:
        control_no: The control number to search for (e.g., "OTH-251022-2523")
        
    Returns:
        MongoDB _id string if found, None otherwise
    """
    try:
        # Extract date from control_no (format: XXX-YYMMDD-NNNN)
        parts = control_no.split('-')
        if len(parts) != 3:
            logger.warning(f"Invalid control_no format: {control_no}")
            return None
        
        date_str = parts[1]  # YYMMDD
        
        # Parse date and create date range (same day)
        try:
            year = int('20' + date_str[0:2])
            month = int(date_str[2:4])
            day = int(date_str[4:6])
            
            # Create date range for that specific day
            target_date = datetime(year, month, day)
            start_date = target_date.strftime('%Y-%m-%dT00:00:00.000Z')
            end_date = (target_date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00.000Z')
            
        except (ValueError, IndexError) as e:
            logger.error(f"Failed to parse date from control_no {control_no}: {e}")
            # Fallback: use a wide date range (last 12 months)
            end_date = datetime.now().strftime('%Y-%m-%dT23:59:59.999Z')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%dT00:00:00.000Z')
        
        # Build API URL with date filters
        date_params = f"date_created_from={start_date}&date_created_to={end_date}"
        api_url = f"{MYNAGA_API_BASE}?{date_params}&{FIXED_QUERY_PARAMS}"
        
        logger.info(f"Fetching MyNaga reports for control_no: {control_no}")
        logger.debug(f"API URL: {api_url}")
        
        # Make API request
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(api_url, headers=headers) as response:
                response_text = await response.text()
                
                if response.status == 401:
                    logger.error(f"MyNaga API authentication failed (401)")
                    logger.debug(f"Response: {response_text[:200]}")
                    return None
                    
                if response.status != 200:
                    logger.error(f"MyNaga API error: {response.status}")
                    logger.debug(f"Response: {response_text[:200]}")
                    return None
                
                try:
                    data = await response.json()
                except:
                    # If response is not JSON, parse the text we already got
                    import json
                    data = json.loads(response_text)
                    
                # MyNaga API returns array directly, not wrapped in {data: [...]}
                if isinstance(data, list):
                    reports = data
                else:
                    reports = data.get('data', [])
                
                # Search for matching control_number
                for report in reports:
                    report_control_no = report.get('control_number', '').strip()
                    if report_control_no == control_no:
                        mongo_id = report.get('_id', '').strip()
                        if mongo_id:
                            logger.info(f"✓ Found MongoDB ID for {control_no}: {mongo_id}")
                            return mongo_id
                
                logger.warning(f"Control number {control_no} not found in {len(reports)} reports")
                return None
                
    except Exception as e:
        logger.error(f"Error fetching MyNaga report ID for {control_no}: {e}")
        return None


async def get_mynaga_report_link(control_no: str) -> Optional[str]:
    """
    Get the full MyNaga report URL for a control number.
    
    Args:
        control_no: The control number to search for
        
    Returns:
        Full MyNaga report URL if found, None otherwise
    """
    mongo_id = await get_mynaga_report_id(control_no)
    if mongo_id:
        return f"https://mynaga.app/reports?_id={mongo_id}"
    return None
