# Case Detail View - MyNaga App Integration

## Overview
Added a professional case detail view that displays complete information from MyNaga App reports, including a direct link to view the original report on the MyNaga App website.

---

## ✨ New Features

### **1. Detailed Case View Modal**
When you click on any case in the Cases table, you now see a **beautiful, detailed view** with:

#### **Header Section**
- Case control number (e.g., "OTH-250918-1511")
- Gradient blue background (government-style)
- Close button

#### **MyNaga App Status Banner**
- Displays current MyNaga App Status with color-coded badge
- **"View in MyNaga App" button** - Opens the original report in a new tab
- Uses the link from column L (Link to report)

#### **Reported Information Section**
Displays all key information with icons:
- 📅 **Created**: Date and time (e.g., "10-09-2025 11:21AM")
- 📍 **Location**: GPS coordinates or address (e.g., "J57M+G2W, Mabolo, Naga City, Bicol")
- 📍 **Barangay**: Barangay name (e.g., "Mabolo")
- ⚠️ **Priority**: Priority level (currently "--" placeholder)
- 👤 **Submitted by**: Reporter's name (e.g., "Leo Paulo Del Rosario")
- 📞 **Contact Number**: Phone number (e.g., "+639634716911")
- 📝 **Category**: Case category (e.g., "Other Public Safety Concerns")
- 📄 **Description**: Full detailed description with line breaks preserved

#### **Additional Information Section**
Displays system data in a grid:
- **Status**: OPEN, RESOLVED, or FOR REROUTING (color-coded badge)
- **Case Aging**: Number of days since creation
- **Month**: Month of creation
- **Refined Category**: More specific category
- **Screened By**: Staff who screened the case
- **Last Update**: Date of last status change

#### **Footer Actions**
- **Edit Case** button - Switches to edit mode
- **Close** button - Returns to cases list

---

## 🔗 MyNaga App Link Integration

### **How It Works**

1. **Data Source**: Column L in Google Sheets ("Link to report")
2. **Database Field**: `link_to_report` in cases table
3. **Display**: Blue button with external link icon

### **Example Link**
```
https://mynaga.ph/reports/12345
```

When clicked:
- Opens in new browser tab
- Takes user directly to the MyNaga App report page
- Shows the original report with all media attachments

---

## 🎨 Visual Design

### **Color Scheme (Professional Government Style)**

#### Status Badges:
- **In Progress**: Blue (bg-blue-100, text-blue-800, border-blue-300)
- **Pending Confirmation**: Amber (bg-amber-100, text-amber-800, border-amber-300)
- **Resolved**: Green (bg-green-100, text-green-800, border-green-300)
- **No Status Yet**: Gray (bg-gray-100, text-gray-800, border-gray-300)
- **Under Review**: Indigo (bg-indigo-100, text-indigo-800, border-indigo-300)
- **Rejected**: Red (bg-red-100, text-red-800, border-red-300)

#### Layout:
- **Header**: Blue gradient (from-blue-700 to-blue-800)
- **Sections**: White background with gray borders
- **Icons**: Gray-400 for consistency
- **Buttons**: Blue-600 primary, Gray-200 secondary

---

## 📋 Example Case Display

### **Case: Illegal Terminal Report**

```
╔══════════════════════════════════════════════════════════╗
║  Case Details                                      ✕     ║
║  Control No: OTH-250918-1511                            ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  MyNaga App Status                                       ║
║  [Pending Confirmation]       [View in MyNaga App →]    ║
║                                                          ║
║  ┌────────────────────────────────────────────────────┐ ║
║  │ Reported Information                               │ ║
║  ├────────────────────────────────────────────────────┤ ║
║  │ 📅 Created                                         │ ║
║  │    10-09-2025 11:21AM                              │ ║
║  │                                                    │ ║
║  │ 📍 Location                                        │ ║
║  │    J57M+G2W, Mabolo, Naga City, Bicol              │ ║
║  │                                                    │ ║
║  │ 📍 Barangay                                        │ ║
║  │    Mabolo                                          │ ║
║  │                                                    │ ║
║  │ ⚠️ Priority                                         │ ║
║  │    --                                              │ ║
║  │                                                    │ ║
║  │ 👤 Submitted by                                    │ ║
║  │    Leo Paulo Del Rosario                           │ ║
║  │                                                    │ ║
║  │ 📞 Contact Number                                  │ ║
║  │    +639634716911                                   │ ║
║  │                                                    │ ║
║  │ 📝 Category                                        │ ║
║  │    Other Public Safety Concerns                    │ ║
║  │                                                    │ ║
║  │ 📄 Description                                     │ ║
║  │    Illegal Terminal at Barangay Mabulo along      │ ║
║  │    Maharlika Highway / Observation that poses     │ ║
║  │    hazard for passengers and riding public in     │ ║
║  │    the area cause traffic flow in area            │ ║
║  │    Unauthorized loading, unloading area and       │ ║
║  │    Uturns of tricycles along the barangay         │ ║
║  │    mabulo area result traffic obstruction and     │ ║
║  │    safety risks to public and fast moving long    │ ║
║  │    vehicles                                        │ ║
║  └────────────────────────────────────────────────────┘ ║
║                                                          ║
║  ┌────────────────────────────────────────────────────┐ ║
║  │ Additional Information                             │ ║
║  ├────────────────────────────────────────────────────┤ ║
║  │ Status: [OPEN]           Case Aging: 43 days      │ ║
║  │ Month: September         Refined Category: --      │ ║
║  └────────────────────────────────────────────────────┘ ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  [Edit Case]                                    [Close]  ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🛠️ Technical Implementation

### **Frontend Component: CaseModal.jsx**

#### **View Modes**
```javascript
const [viewMode, setViewMode] = useState('view') // 'view' or 'edit'

// Default behavior:
// - Existing case: Opens in 'view' mode (read-only)
// - New case: Opens in 'edit' mode (form)
```

#### **Date Formatting**
```javascript
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    month: '2-digit',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}
// Output: "10-09-2025 11:21AM"
```

#### **Status Badge Colors**
```javascript
const getStatusColor = (status) => {
  const colors = {
    'In Progress': 'bg-blue-100 text-blue-800 border-blue-300',
    'Pending Confirmation': 'bg-amber-100 text-amber-800 border-amber-300',
    'Resolved': 'bg-green-100 text-green-800 border-green-300',
    // ... etc
  }
  return colors[status] || 'bg-gray-100 text-gray-800 border-gray-300'
}
```

#### **External Link Button**
```jsx
{caseData.link_to_report && (
  <a
    href={caseData.link_to_report}
    target="_blank"
    rel="noopener noreferrer"
    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
  >
    <FiExternalLink />
    View in MyNaga App
  </a>
)}
```

---

## 📊 Data Flow

### **From Google Sheets to Display**

1. **Google Sheets** (Main tab)
   - Column L: "Link to report"
   - Example: `https://mynaga.ph/reports/12345`

2. **Backend Sync** (google_sheets_sync.py)
   - Maps column L → `link_to_report` field
   - Syncs every 10 seconds

3. **Database** (SQLite)
   - Table: `cases`
   - Field: `link_to_report` (TEXT)

4. **API Response** (/api/cases)
   ```json
   {
     "id": 1234,
     "control_no": "OTH-250918-1511",
     "link_to_report": "https://mynaga.ph/reports/12345",
     "mynaga_app_status": "Pending Confirmation",
     "description": "Illegal Terminal at Barangay Mabulo...",
     ...
   }
   ```

5. **Frontend Display** (CaseModal.jsx)
   - Shows all fields in organized sections
   - "View in MyNaga App" button links to report

---

## 🔄 User Workflow

### **Viewing a Case**

1. **Navigate to Cases page**
   ```
   http://localhost:3000/cases
   ```

2. **Click on any case row** in the table

3. **Case Detail Modal opens** in "View Mode"
   - See all reported information
   - See additional system information
   - See MyNaga App status with badge

4. **Click "View in MyNaga App"** (if link exists)
   - Opens MyNaga App report in new tab
   - View original submission with photos/videos

5. **Click "Edit Case"** (optional)
   - Switches to edit mode
   - Can update case information

6. **Click "Close"**
   - Returns to cases list

---

## ✅ Features Checklist

- [x] Professional government-style design
- [x] Read-only view mode by default
- [x] All MyNaga report fields displayed
- [x] Color-coded MyNaga status badges
- [x] External link to MyNaga App report
- [x] Icon-based layout for clarity
- [x] Date formatting (MM-DD-YYYY HH:MMAM/PM)
- [x] Description with preserved line breaks
- [x] Additional information grid
- [x] Edit mode toggle
- [x] Responsive modal (max 90% viewport height)
- [x] Smooth animations and transitions

---

## 🎯 Benefits

### **For Users:**
1. **Complete Information** - See all case details at a glance
2. **Easy Access** - One click to view original MyNaga report
3. **Professional Look** - Clean, organized, government-style interface
4. **Quick Navigation** - Switch between view and edit modes

### **For Administration:**
1. **Verification** - Easily verify case details against MyNaga App
2. **Contact** - Quickly find reporter contact information
3. **Tracking** - See case aging and status updates
4. **Integration** - Seamless connection to MyNaga App platform

---

## 📝 Example Use Cases

### **Use Case 1: Verify Report Details**
```
1. Citizen calls about their report
2. Staff opens Cases page
3. Searches for case by control number
4. Clicks case to view details
5. Confirms information with citizen
6. Clicks "View in MyNaga App" to see photos
7. Updates case status if needed
```

### **Use Case 2: Follow Up on Pending Cases**
```
1. Click "Pending Confirmation" on dashboard
2. See filtered list of pending cases
3. Click first case to view details
4. See full description and reporter info
5. Click "View in MyNaga App" for context
6. Contact reporter using displayed phone number
7. Update status to "In Progress"
```

### **Use Case 3: Review Case History**
```
1. Open case detail modal
2. Review "Created" date (when reported)
3. Check "Last Update" date
4. See "Case Aging" (days open)
5. Understand timeline of case
6. Make informed decision on next action
```

---

## 🚀 Testing

### **Test the Feature:**

1. **Open Dashboard**
   ```
   http://localhost:3000
   ```

2. **Click "In Progress" status card**
   - Navigate to filtered cases

3. **Click any case in the table**
   - Case detail modal should open
   - Should show "View Mode" with all details

4. **Verify Information Display:**
   - ✅ MyNaga status badge shows correct color
   - ✅ Created date formatted correctly
   - ✅ Location and barangay displayed
   - ✅ Reporter name and contact visible
   - ✅ Full description with line breaks
   - ✅ Additional info grid populated

5. **Test MyNaga App Link:**
   - ✅ "View in MyNaga App" button appears (if link exists)
   - ✅ Clicking opens new tab
   - ✅ Link goes to correct MyNaga report

6. **Test Edit Mode:**
   - ✅ Click "Edit Case" button
   - ✅ Modal switches to form view
   - ✅ All fields editable
   - ✅ Click "Cancel" returns to view mode

---

## 📋 Summary

**Feature:** Case Detail View with MyNaga App Integration  
**Purpose:** Display complete case information from MyNaga App reports  
**Key Feature:** Direct link to original MyNaga App report  
**Design:** Professional, government-style, clean interface  
**Status:** ✅ **READY TO USE**

Users can now click any case to see **complete reported information** including the full description, reporter details, and a **direct link to view the original MyNaga App report**! 🎉
