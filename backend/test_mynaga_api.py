#!/usr/bin/env python3
"""
Manual script to test MyNaga API and see what data is available
"""

import requests
import json

# Your MyNaga token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OGE0ODk3Zjg1ZmIxYTdiYjU2YTNjYTQiLCJpYXQiOjE3NjA1ODE1NDgsImV4cCI6MTc2MTE4NjM0OH0.AlIem843s3R_SaGLQVMjP3EfYaVMrOKANoVYv7zX3ns"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("🔍 Testing MyNaga API endpoints...\n")

# Try different possible endpoints
endpoints = [
    "https://mynaga.app/api/reports",
    "https://mynaga.app/api/reports?limit=5",
    "https://mynaga.app/api/report",
    "https://mynaga.app/api/cases",
    "https://mynaga.app/api/v1/reports",
    "https://api.mynaga.app/reports",
]

for endpoint in endpoints:
    print(f"Testing: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  ✅ SUCCESS! Response type: {type(data)}")
                
                # Pretty print first item
                if isinstance(data, list) and len(data) > 0:
                    print(f"  Total items: {len(data)}")
                    print(f"  First item keys: {list(data[0].keys())}")
                    print(f"\n  Sample record:")
                    print(json.dumps(data[0], indent=2))
                elif isinstance(data, dict):
                    print(f"  Response keys: {list(data.keys())}")
                    print(f"\n  Full response:")
                    print(json.dumps(data, indent=2)[:1000])
                
                print("\n" + "="*60 + "\n")
                break  # Found working endpoint!
                
            except json.JSONDecodeError:
                print(f"  Response is not JSON: {response.text[:200]}")
        elif response.status_code == 401:
            print(f"  ❌ Unauthorized - Token might be expired")
        elif response.status_code == 404:
            print(f"  ⚠️  Not Found - Try different endpoint")
        else:
            print(f"  ⚠️  Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print()

print("\n💡 Instructions:")
print("1. If you see '✅ SUCCESS!' above, check the sample record")
print("2. Look for fields like: _id, control_no, controlNo, caseId, etc.")
print("3. Share the sample record structure with me")
print("4. I'll update the fetch_mynaga_ids.py script to match")
print("\nIf all endpoints fail:")
print("1. Token might be expired - get a new one from MyNaga")
print("2. Ask MyNaga team: 'What's the API endpoint to list all reports?'")
print("3. Or check MyNaga's API documentation")
