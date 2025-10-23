# 🔗 MyNaga Real-Time Integration Guide

## What's New

Your MyNaga Dashboard now supports **real-time data synchronization** directly from the MyNaga App API! No more manual Excel imports - your data updates automatically.

## ✨ Features

✅ **Real-time Sync** - Data updates automatically every 5 minutes (configurable)
✅ **Background Jobs** - Runs in the background without interrupting your work
✅ **Auto Mapping** - Automatically maps MyNaga data to your dashboard
✅ **Connection Testing** - Test your token before enabling sync
✅ **Manual Sync** - Sync on-demand anytime
✅ **Sync Status** - View sync history and statistics
✅ **Error Handling** - Clear error messages if anything fails

## 🚀 Getting Started

### Step 1: Get Your MyNaga Auth Token

1. Open **MyNaga App**
2. Go to **Settings** → **API** → **Generate Token**
3. Copy the authentication token
4. Keep it safe (like a password)

### Step 2: Configure in Dashboard

1. Open your dashboard: `http://localhost:3000`
2. Click **"MyNaga Sync"** in the sidebar (⚡ icon)
3. Paste your auth token in the text area
4. (Optional) Change sync interval (default: 5 minutes)
5. Click **"Test Connection"** to verify
6. Click **"Configure MyNaga Connection"**

### Step 3: Start Syncing

✅ Done! Your data will now sync automatically every 5 minutes.

View the sync status on the right panel to see:
- Last sync time
- Number of records created/updated
- Any errors

## 📊 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     Your Computer                               │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Your MyNaga Dashboard (Frontend)                         │  │
│  │  - View all cases                                         │  │
│  │  - Create clusters & tags                                │  │
│  │  - Track progress                                         │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Your Dashboard Backend (Python)                         │  │
│  │  - Background scheduler (every 5 min)                   │  │
│  │  - Fetches new data from MyNaga                         │  │
│  │  - Updates local database                               │  │
│  │  - Stores all data locally                              │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                    HTTP API Calls
                     (with token)
                            │
        ┌───────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MyNaga.app (Cloud)                           │
│                                                                  │
│  - All the reports data                                         │
│  - Real reports submitted by users                             │
│  - Status updates                                              │
│  - Attachments & media                                         │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Sync Workflow

```
1. Dashboard starts → Scheduler initialized
                ↓
2. Every 5 minutes (or your interval)
                ↓
3. Background job triggers
                ↓
4. Fetches new/updated reports from MyNaga API
                ↓
5. For each report:
   - Check if already in database
   - Create new case or update existing
   - Map MyNaga fields to local fields
                ↓
6. Save all to database
                ↓
7. Display sync status (created: X, updated: Y, errors: Z)
                ↓
8. Wait for next interval and repeat
```

## 🗂️ Data Mapping

Your MyNaga reports are automatically mapped to case fields:

| MyNaga Field | Dashboard Field | Notes |
|---|---|---|
| id | Control No. | Unique identifier |
| createdAt | Date Created | Report creation date |
| category | Category | Issue category |
| location | Sender's Location | Where reported from |
| barangay | Barangay | Barangay name |
| description | Description | Full report text |
| attachments | Attached Media | Photos/videos |
| reporterName | Reported by | Who submitted |
| reporterPhone | Contact Number | Reporter's phone |
| url | Link to Report | Original link |
| status | MyNaga App Status | Status from MyNaga |
| refinedCategory | Refined Category | Categorized type |
| status (mapped) | Status | OPEN/RESOLVED/FOR REROUTING |

## ⚙️ Configuration Options

### Sync Interval

Default: **5 minutes**

Options: 1, 2, 5, 10, 15, 30, 60 minutes

**Recommendation:**
- **1-5 min**: Real-time feel (uses more bandwidth)
- **5-10 min**: Balance between fresh data and efficiency
- **30-60 min**: Minimal server load, less frequent updates

### Manual Sync

Don't want to wait? Click **"Sync Now"** button to fetch immediately.

Useful for:
- Testing your setup
- Getting urgent updates
- Troubleshooting issues

## 📊 Sync Status Dashboard

View real-time sync information on the MyNaga Sync page:

**Status Indicator**
- ✅ Ready - Sync is configured and working
- 🔄 Syncing - Currently fetching data
- ❌ Error - Last sync had issues

**Last Sync Info**
- When the last sync occurred
- Number of records created
- Number of records updated
- Any errors that occurred

**Latest Stats**
- Total reports fetched
- New cases created
- Existing cases updated
- Failed processes

## 🔐 Security & Privacy

✅ **Secure Storage**
- Your token is sent only to MyNaga API
- Token is NOT stored in plain text
- All data stays on your local server

✅ **Data Privacy**
- No data sent to third parties
- All sync happens locally
- You control your data

✅ **Token Safety**
- Keep your token private (like a password)
- Generate new token if compromised
- Can revoke tokens in MyNaga Settings

## ❓ Troubleshooting

### "Connection Failed" Error

**Possible causes:**
1. Internet connection issue
2. Invalid token
3. Token has wrong permissions
4. MyNaga API temporarily down

**Solution:**
1. Check internet connection
2. Verify token is correct
3. Check token has API access permission
4. Try again in a few minutes

### No Data Syncing

**Possible causes:**
1. Sync not configured
2. No new reports on MyNaga
3. Scheduler not running
4. Token expired

**Solution:**
1. Go to MyNaga Sync page
2. Click "Test Connection"
3. Try "Sync Now" button
4. Check backend logs

### Sync Stopped Working

**Possible causes:**
1. Token expired or revoked
2. Server restarted
3. Network issue
4. API changes

**Solution:**
1. Test connection again
2. Reconfigure if needed
3. Check internet
4. View error messages

## 📚 API Endpoints

All new endpoints start with `/api/mynaga/`:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/config` | Configure MyNaga connection |
| POST | `/test-connection` | Test auth token |
| POST | `/sync/manual` | Trigger immediate sync |
| GET | `/sync/status` | Get sync status |
| POST | `/sync/stop` | Stop the scheduler |

## 🎯 Use Cases

### Real Estate Agent
- Property reports sync automatically
- See new leads in real-time
- Track resolution status
- No manual data entry

### City Administrator
- All citizen reports auto-imported
- Automatic categorization
- See trending issues
- Track department response

### Emergency Response
- Urgent reports appear instantly
- Team sees real-time updates
- Automatic clustering by location
- Fast response coordination

### Customer Support
- Reports automatically organized
- No data entry delays
- Real-time tracking
- Historical data preserved

## 🚀 Advanced Features

### Automatic Clustering
- Reports automatically grouped by location
- Similar issues identified
- Batch responses possible

### Status Tracking
- Track from report → resolution
- See all status changes
- Calculate average response time

### Historical Data
- All data kept locally
- No data loss
- Full audit trail
- Export anytime

### Custom Filtering
- Filter by status
- Filter by category
- Filter by barangay
- Search by description

## ⚡ Performance Tips

1. **Set appropriate sync interval**
   - Too frequent: High bandwidth/CPU
   - Too infrequent: Delayed data

2. **Use manual sync strategically**
   - Test new setup
   - Emergency updates
   - Troubleshooting

3. **Monitor sync status**
   - Check for errors
   - Verify data counts
   - Track history

4. **Regular exports**
   - Backup your data
   - Create reports
   - Share with team

## 📞 Still Need Help?

1. Check the sync status dashboard
2. Test your connection
3. Review error messages
4. Check your internet connection
5. Verify token is valid
6. Try manual sync
7. Check backend logs

---

## 🎉 You're All Set!

Your dashboard now has **real-time MyNaga integration**! 

Data will automatically sync every 5 minutes (or your chosen interval). Watch your data update in real-time as new reports come in.

**Happy syncing!** ⚡
