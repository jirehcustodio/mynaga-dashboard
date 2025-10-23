# Clickable Status Filtering Feature Guide

## 📋 Overview

The MyNaga Status Dashboard now includes **clickable status cards** that allow users to instantly navigate to a filtered view of cases based on their MyNaga App Status.

---

## 🎯 How It Works

### **User Interaction Flow**

1. **View Dashboard**
   - User sees 6 status cards with case counts
   - Each card shows: Status name, count, percentage, description

2. **Click Status Card**
   - User clicks on any status card (e.g., "In Progress")
   - System navigates to: `/cases?mynaga_status=In Progress`

3. **View Filtered Cases**
   - Cases page loads with automatic filter applied
   - Only cases with matching `mynaga_app_status` are displayed
   - Filter badge shows: "Filtered by MyNaga Status: In Progress"

4. **Clear Filter**
   - User clicks ✕ button on filter badge
   - All cases are displayed again
   - URL changes back to `/cases`

---

## 💻 Technical Implementation

### **MyNagaStatusCard.jsx**

#### Import React Router
```javascript
import { useNavigate } from 'react-router-dom';
```

#### Create Navigation Handler
```javascript
const navigate = useNavigate();

const handleStatusClick = (statusName) => {
  navigate(`/cases?mynaga_status=${encodeURIComponent(statusName)}`);
};
```

#### Update Card Click Handler
```javascript
<button
  onClick={() => handleStatusClick(item.name)}
  className="status-card-button"
>
  {/* Card content */}
</button>
```

---

### **CasesPage.jsx**

#### Import URL Parameter Handling
```javascript
import { useSearchParams } from 'react-router-dom';
```

#### Setup State and URL Monitoring
```javascript
const [searchParams, setSearchParams] = useSearchParams();
const [mynagaStatusFilter, setMynagaStatusFilter] = useState('');

useEffect(() => {
  const statusFromUrl = searchParams.get('mynaga_status');
  if (statusFromUrl) {
    setMynagaStatusFilter(statusFromUrl);
  }
}, [searchParams]);
```

#### Filter Cases
```javascript
const loadCases = async () => {
  const res = await caseAPI.getAll(0, 100, {...filters});
  
  // Apply MyNaga status filter
  let filteredCases = res.data;
  if (mynagaStatusFilter) {
    filteredCases = res.data.filter(
      c => c.mynaga_app_status === mynagaStatusFilter
    );
  }
  
  setCases(filteredCases);
};
```

#### Display Filter Badge
```javascript
{mynagaStatusFilter && (
  <div className="filter-badge">
    <span>Filtered by MyNaga Status:</span>
    <span className="font-semibold">{mynagaStatusFilter}</span>
    <button onClick={() => {
      setMynagaStatusFilter('');
      setSearchParams({});
    }}>
      ✕
    </button>
  </div>
)}
```

---

## 🔗 URL Structure

### **Dashboard URL**
```
http://localhost:3000/
```

### **Filtered Cases URLs**
```
http://localhost:3000/cases?mynaga_status=In%20Progress
http://localhost:3000/cases?mynaga_status=Pending%20Confirmation
http://localhost:3000/cases?mynaga_status=Resolved
http://localhost:3000/cases?mynaga_status=No%20Status%20Yet
http://localhost:3000/cases?mynaga_status=Under%20Review
http://localhost:3000/cases?mynaga_status=Rejected
```

**Note:** Status names with spaces are URL-encoded (`%20`)

---

## 📊 Status Mapping

| Status Card | Filter Value | Database Field |
|-------------|--------------|----------------|
| In Progress | `"In Progress"` | `mynaga_app_status = "In Progress"` |
| Pending Confirmation | `"Pending Confirmation"` | `mynaga_app_status = "Pending Confirmation"` |
| Resolved | `"Resolved"` | `mynaga_app_status = "Resolved"` |
| No Status Yet | `"No Status Yet"` | `mynaga_app_status = "No Status Yet"` |
| Under Review | `"Under Review"` | `mynaga_app_status = "Under Review"` |
| Rejected | `"Rejected"` | `mynaga_app_status = "Rejected"` |

---

## 🎨 Visual Indicators

### **Status Card (Clickable)**
```
┌───────────────────────────────────┐
│ ● IN PROGRESS                  → │  ← Arrow on hover
│ Cases currently being processed   │
│                                   │
│ 908                               │
│ ████████████░░░░░░░░░ 39.1%      │
└───────────────────────────────────┘
     Cursor: pointer
     Hover: Lift effect + shadow
```

### **Filter Badge (Cases Page)**
```
┌─────────────────────────────────────────────┐
│ Cases                                        │
│ ┌───────────────────────────────────────┐   │
│ │ Filtered by MyNaga Status: In Progress ✕│ │
│ └───────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
     ✕ = Clear filter button
```

---

## 🔍 Example User Scenarios

### **Scenario 1: Check In Progress Cases**
```
1. User opens dashboard
2. Sees "In Progress: 908"
3. Clicks the card
4. Navigates to /cases?mynaga_status=In%20Progress
5. Sees 908 filtered cases
6. Can click ✕ to view all cases again
```

### **Scenario 2: Review Rejected Cases**
```
1. User opens dashboard
2. Sees "Rejected: 37"
3. Clicks the card
4. Navigates to /cases?mynaga_status=Rejected
5. Reviews all 37 rejected cases
6. Can take action on specific cases
```

### **Scenario 3: Monitor Pending Confirmations**
```
1. User opens dashboard
2. Sees "Pending Confirmation: 476"
3. Clicks the card
4. Views all cases awaiting confirmation
5. Can follow up on pending items
```

---

## ⚙️ Configuration

### **Enable/Disable Filtering**

To disable filtering (show all cases):
```javascript
// In CasesPage.jsx
const loadCases = async () => {
  const res = await caseAPI.getAll(0, 100, {...filters});
  // Comment out filter logic
  // let filteredCases = res.data;
  // if (mynagaStatusFilter) { ... }
  setCases(res.data); // Show all cases
};
```

### **Add Additional Filters**

To filter by multiple criteria:
```javascript
let filteredCases = res.data;

// Filter by MyNaga status
if (mynagaStatusFilter) {
  filteredCases = filteredCases.filter(
    c => c.mynaga_app_status === mynagaStatusFilter
  );
}

// Add another filter (e.g., barangay)
if (barangayFilter) {
  filteredCases = filteredCases.filter(
    c => c.barangay === barangayFilter
  );
}
```

---

## 🐛 Troubleshooting

### **Issue: Filter not working**
**Solution:** Check that `mynaga_app_status` field exists in case data
```javascript
console.log('First case:', cases[0]);
// Should show: mynaga_app_status: "In Progress"
```

### **Issue: Navigation not working**
**Solution:** Verify React Router is properly configured
```javascript
// In App.jsx, ensure Routes are set up:
<Route path="/cases" element={<CasesPage />} />
```

### **Issue: Filter badge not appearing**
**Solution:** Check URL parameters
```javascript
console.log('URL params:', searchParams.get('mynaga_status'));
console.log('Filter state:', mynagaStatusFilter);
```

---

## ✅ Testing Checklist

- [ ] Click each status card and verify navigation
- [ ] Confirm URL updates with correct query parameter
- [ ] Verify filter badge appears with correct status name
- [ ] Confirm cases are filtered correctly
- [ ] Test clear filter button (✕)
- [ ] Verify all cases appear after clearing filter
- [ ] Test with different status combinations
- [ ] Verify URL encoding for spaces (e.g., "In Progress")
- [ ] Test browser back/forward buttons
- [ ] Confirm filter persists on page refresh

---

## 📈 Performance Considerations

### **Client-Side Filtering**
- ✅ Fast response (no API call needed)
- ✅ Works with existing data
- ✅ No server load

### **Potential Improvements**
1. **Server-Side Filtering** (for large datasets)
   ```javascript
   // Modify API call to include mynaga_status filter
   const res = await caseAPI.getAll(0, 100, {
     ...filters,
     mynaga_app_status: mynagaStatusFilter
   });
   ```

2. **Add Loading State**
   ```javascript
   const [isFiltering, setIsFiltering] = useState(false);
   ```

3. **Cache Filtered Results**
   ```javascript
   const [cachedFilters, setCachedFilters] = useState({});
   ```

---

## 🎓 Best Practices

1. **Always URL-encode status names**
   ```javascript
   encodeURIComponent(statusName)
   ```

2. **Clear filter when navigating away**
   ```javascript
   useEffect(() => {
     return () => setMynagaStatusFilter('');
   }, []);
   ```

3. **Provide visual feedback**
   - Hover effects on cards
   - Filter badge on cases page
   - Arrow indicator (→)

4. **Handle edge cases**
   - Empty filter results
   - Invalid status names
   - Multiple filters

---

## 📝 Summary

The clickable status filtering feature provides:
- ✅ **One-click access** to filtered case views
- ✅ **Clear visual indicators** (hover effects, badges)
- ✅ **Professional navigation** (React Router integration)
- ✅ **Easy filter management** (clear button)
- ✅ **URL-based filtering** (shareable links)
- ✅ **Fast performance** (client-side filtering)

**Result:** Users can instantly navigate to specific case categories with a single click, improving workflow efficiency and user experience.
