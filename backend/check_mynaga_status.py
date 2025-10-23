"""Check MyNaga App Status column variants."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Load credentials
CREDENTIALS_PATH = '/Users/jirehb.custodio/Downloads/mynagaapp-sheets-api-c06bb9d76039.json'
SPREADSHEET_ID = '1c9OgQ_fr-Ia33wnXh3tC1JTh8hyaSoOIwME0RrAG7Uo'

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# Get sheet name from gid
metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
sheet_name = None
for s in metadata['sheets']:
    if s['properties']['sheetId'] == 412096204:
        sheet_name = s['properties']['title']
        break

print(f"Reading from sheet: '{sheet_name}'")

# Read data
result = sheet.values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f"'{sheet_name}'"
).execute()

data = result.get('values', [])
headers = data[0] if data else []

# Find MyNaga App Status column
mynaga_status_idx = None
for i, header in enumerate(headers):
    if 'MyNaga App Status' in str(header):
        mynaga_status_idx = i
        print(f"\n✅ Found 'MyNaga App Status' at column index: {i}")
        print(f"   Column name: '{header}'")
        break

if mynaga_status_idx is not None:
    # Extract all values
    status_values = []
    for row in data[1:]:
        if len(row) > mynaga_status_idx:
            val = str(row[mynaga_status_idx]).strip()
            if val:
                status_values.append(val)
    
    # Get unique values
    unique_statuses = sorted(set(status_values))
    
    print(f"\n📊 UNIQUE VALUES in 'MyNaga App Status' column:")
    print(f"   Total unique variants: {len(unique_statuses)}\n")
    
    for i, status in enumerate(unique_statuses, 1):
        count = status_values.count(status)
        print(f"   {i}. '{status}' - ({count} cases)")
    
    print(f"\n   Total non-empty values: {len(status_values)}")
    print(f"   Total rows (excluding header): {len(data) - 1}")
else:
    print("\n❌ Column 'MyNaga App Status' not found")
    print("\nAvailable columns (first 20):")
    for i, col in enumerate(headers[:20]):
        print(f"   {i}: '{col}'")
