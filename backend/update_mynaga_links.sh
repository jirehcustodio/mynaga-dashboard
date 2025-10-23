#!/bin/bash
# Quick script to update MyNaga links in Google Sheets
#
# Usage: bash update_mynaga_links.sh

echo "🔗 MyNaga Link Updater"
echo "====================="
echo ""
echo "This will fetch report data from MyNaga API and update Column L in your Google Sheet"
echo ""

# Your Google Spreadsheet ID (get it from the URL)
# Example URL: https://docs.google.com/spreadsheets/d/1AbC123XyZ456.../edit
# SPREADSHEET_ID is: 1AbC123XyZ456...
SPREADSHEET_ID="YOUR_SPREADSHEET_ID_HERE"

# Date range (adjust as needed)
START_DATE="2025-08-01"
END_DATE="2025-10-31"

if [ "$SPREADSHEET_ID" = "YOUR_SPREADSHEET_ID_HERE" ]; then
    echo "❌ Error: Please edit this script and set your SPREADSHEET_ID"
    echo ""
    echo "1. Open your Google Sheet"
    echo "2. Copy the ID from the URL"
    echo "3. Edit this script: nano update_mynaga_links.sh"
    echo "4. Replace YOUR_SPREADSHEET_ID_HERE with your actual ID"
    exit 1
fi

echo "📊 Spreadsheet ID: $SPREADSHEET_ID"
echo "📅 Date Range: $START_DATE to $END_DATE"
echo ""
echo "Starting in 3 seconds... (Ctrl+C to cancel)"
sleep 3

python3 fetch_mynaga_ids.py "$SPREADSHEET_ID" "$START_DATE" "$END_DATE"
