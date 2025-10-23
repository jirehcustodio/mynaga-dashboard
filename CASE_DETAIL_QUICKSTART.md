# Quick Guide: View Case Details

## 🎯 How to View Case Details

### **Step 1: Open Cases Page**
Navigate to: `http://localhost:3000/cases`

### **Step 2: Click Any Case**
Click on any row in the cases table

### **Step 3: View Details**
A professional modal will open showing:

```
┌─────────────────────────────────────────────────┐
│ Case Details                              ✕     │
│ Control No: OTH-250918-1511                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ MyNaga App Status                               │
│ [Pending Confirmation] [View in MyNaga App →]  │
│                                                 │
│ ╔═══════════════════════════════════════════╗  │
│ ║ Reported Information                      ║  │
│ ╠═══════════════════════════════════════════╣  │
│ ║ 📅 Created: 10-09-2025 11:21AM            ║  │
│ ║ 📍 Location: J57M+G2W, Mabolo...          ║  │
│ ║ 📍 Barangay: Mabolo                       ║  │
│ ║ 👤 Submitted by: Leo Paulo Del Rosario    ║  │
│ ║ 📞 Contact: +639634716911                 ║  │
│ ║ 📝 Category: Other Public Safety          ║  │
│ ║ 📄 Description: Illegal Terminal at...    ║  │
│ ╚═══════════════════════════════════════════╝  │
│                                                 │
│ ╔═══════════════════════════════════════════╗  │
│ ║ Additional Information                    ║  │
│ ╠═══════════════════════════════════════════╣  │
│ ║ Status: [OPEN]    Case Aging: 43 days    ║  │
│ ║ Month: September  Refined Cat: --         ║  │
│ ╚═══════════════════════════════════════════╝  │
│                                                 │
├─────────────────────────────────────────────────┤
│ [Edit Case]                          [Close]    │
└─────────────────────────────────────────────────┘
```

---

## 🔗 View Original MyNaga Report

**If the case has a link to the MyNaga App:**

1. Look for the blue button: **"View in MyNaga App →"**
2. Click it to open the original report in a new tab
3. See the report with all photos, videos, and original submission

**Note:** The link comes from column L in your Google Sheet ("Link to report")

---

## ✏️ Edit Case Information

1. Click **"Edit Case"** button at the bottom
2. Modal switches to edit mode (form view)
3. Update any fields needed
4. Click **"Update Case"** to save
5. OR click **"Cancel"** to return to view mode

---

## 📋 What Information is Displayed?

### **Reported Information:**
- ✅ Creation date and time
- ✅ GPS location or address
- ✅ Barangay name
- ✅ Reporter's full name
- ✅ Contact phone number
- ✅ Case category
- ✅ Complete description (with line breaks)

### **Additional Information:**
- ✅ Case status (OPEN/RESOLVED/FOR REROUTING)
- ✅ Case aging (days since creation)
- ✅ Month of creation
- ✅ Refined category
- ✅ Screened by (staff name)
- ✅ Last status update date

### **MyNaga App Integration:**
- ✅ Current MyNaga App status (color-coded badge)
- ✅ Direct link to original MyNaga report

---

## 🎨 Status Badge Colors

- **In Progress**: 🔵 Blue
- **Pending Confirmation**: 🟡 Amber/Yellow
- **Resolved**: 🟢 Green
- **No Status Yet**: ⚪ Gray
- **Under Review**: 🟣 Indigo
- **Rejected**: 🔴 Red

---

## ⌨️ Keyboard Shortcuts

- **ESC**: Close the modal
- **Click outside**: Close the modal

---

## 💡 Tips

1. **Quick Access**: Click any case from the dashboard filtered view
2. **Verify Info**: Use "View in MyNaga App" to see photos/videos
3. **Contact Reporter**: Phone number is readily available
4. **Track Progress**: Check "Case Aging" to see how long it's been open
5. **Update Status**: Click "Edit Case" to change status or add notes

---

## 🚀 Example Workflow

### **Responding to a Citizen Inquiry:**

```
1. Citizen calls: "What's the status of my report about 
   the illegal terminal in Mabolo?"

2. Staff: 
   - Opens http://localhost:3000/cases
   - Searches for "Mabolo" or "illegal terminal"
   - Clicks the case to view details
   
3. Modal shows:
   - Reporter: Leo Paulo Del Rosario
   - Contact: +639634716911
   - Status: Pending Confirmation
   - Description: Full details about illegal terminal
   
4. Staff:
   - Confirms details with citizen
   - Clicks "View in MyNaga App" to verify
   - Updates status to "In Progress"
   - Provides update to citizen

✅ Complete transaction in under 2 minutes!
```

---

## ✅ Summary

**Feature**: Professional case detail viewer  
**Access**: Click any case in the table  
**Shows**: Complete MyNaga App report information  
**Action**: Direct link to original MyNaga report  
**Design**: Clean, government-style interface  

**Now live and ready to use!** 🎉
