# LexAudit Flow - Architecture & Design Document

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Dashboard          PDFViewer         NotificationBadge  │   │
│  │ - Update List      - Highlight View  - Alert Badge     │   │
│  │ - Approval UI      - Accept/Reject                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│              │                    ▲                               │
│              │ HTTP/JSON          │ JSON                          │
│              ▼                    │                               │
├─────────────────────────────────────────────────────────────────┤
│                    FastAPI Backend (Python)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ API Layer                                               │   │
│  │ GET/POST Routes for Updates, Evidence, Crawls         │   │
│  └──────────────────────────────────────────────────────────┘   │
│              │                    │                               │
│              │                    │                               │
│  ┌──────────────────┐  ┌─────────────────────────────────────┐  │
│  │ Agents Module    │  │  Core Module                        │  │
│  │ - crawler.py     │  │  - db.py (MongoDB)                  │  │
│  │ - analyzer.py    │  │  - models.py (Pydantic)            │  │
│  │ - highlighter.py │  │                                     │  │
│  └──────────────────┘  └─────────────────────────────────────┘  │
│       │                           │                               │
└───────┼───────────────────────────┼───────────────────────────────┘
        │                           │
        │ HTTP                      │ TCP
        ▼                           ▼
┌──────────────────┐    ┌──────────────────────────┐
│ Ollama Server    │    │  MongoDB                 │
│ Llama 3.2:3b     │    │  - tax_schemes           │
│ (Local LLM)      │    │  - pending_updates       │
│                  │    │  - audit_logs            │
└──────────────────┘    └──────────────────────────┘
        │                           │
        │ Download PDFs             │ Store Data
        ▼                           ▼
  Government/Tax Websites    Evidence PDFs (local)
```

---

## 🔄 Data Flow

### Workflow 1: Website Crawl & Analysis

```
1. Manager enters URL in frontend
   ↓
2. Frontend sends POST /crawl?url=X to backend
   ↓
3. Crawler agent (Playwright):
   - Visits URL with fake user-agent
   - Finds all PDF links containing tax keywords
   - Downloads PDFs to backend/evidence/raw/
   ↓
4. For each PDF, analyzer agent:
   - Extracts text with PyMuPDF
   - Sends to Ollama (Llama 3.2) with system prompt
   - Ollama responds with JSON: {change_detected, item, new_val, quote}
   ↓
5. If change detected:
   - highlighter agent creates highlighted PDF with quote marked
   - Store record in pending_updates collection
   ↓
6. Frontend polls GET /updates
   - Displays new alerts in dashboard
   - Shows NotificationBadge with count
```

### Workflow 2: Manager Approval/Rejection

```
1. Manager reviews update in dashboard
   ↓
2. Frontend shows:
   - Item name and change details
   - Highlighted PDF with evidence
   ↓
3. Manager clicks "Accept" or "Reject"
   ↓
4. Frontend sends POST /updates/{id}/accept with {accept: true/false}
   ↓
5. Backend processes:
   
   IF ACCEPT:
   ├─ Update tax_schemes: new_value for item
   ├─ Mark update status as "accepted"
   └─ Log to audit_logs: {action, item, old_val, new_val, timestamp}
   
   IF REJECT:
   ├─ Mark update status as "rejected"
   └─ Log to audit_logs: {action, item, old_val, new_val}
   ↓
6. Frontend refreshes updates list
```

---

## 📊 Database Schema

### Collections

#### 1. tax_schemes (Source of Truth)
```javascript
{
  _id: ObjectId,
  item_name: String,          // Unique identifier
  tax_percentage: Float,      // The actual tax rate
  last_updated: DateTime      // When this was last updated
}

// Indexes
- item_name (unique)
```

#### 2. pending_updates (AI Recommendations)
```javascript
{
  _id: ObjectId,
  detected_item: String,                  // From AI analysis
  current_db_val: Float,                  // What's in tax_schemes now
  new_web_val: Float,                     // What AI found
  evidence_pdf_path: String,              // Path to highlighted PDF
  evidence_quote: String,                 // Exact quote from PDF
  status: "pending|accepted|rejected",    // Workflow status
  created_at: DateTime,
  updated_at: DateTime
}

// Indexes
- status
```

#### 3. audit_logs (Complete Audit Trail)
```javascript
{
  _id: ObjectId,
  action: "update_accepted|update_rejected",
  item_name: String,
  old_value: Float,
  new_value: Float,
  timestamp: DateTime,
  manager_id: String (optional)
}

// Indexes
- timestamp (for sorting by recency)
```

---

## 🔐 Security & Constraints

### Constraint: AI Cannot Modify Database

```python
# ❌ FORBIDDEN: Ollama/AI directly updates tax_schemes
db.tax_schemes.update_one(...)  # NOT DONE IN analyzer.py

# ✅ ALLOWED: Only /updates/{id}/accept endpoint updates
db.tax_schemes.update_one(...)  # ONLY in main.py accept endpoint
```

### Limited Update Scope
```python
# Only these fields can be updated:
update_dict = {
    "tax_percentage": new_value,  # ✅ ALLOWED
    # "item_name": new_name,       # ❌ NOT ALLOWED (read-only)
}

# NOT allowed:
# - Deleting tax schemes
# - Adding new fields
# - Modifying item_name
# - Batch updates without individual approval
```

### Audit Trail Requirement
Every decision is logged with:
- Action taken (accept/reject)
- Item name
- Old and new values
- Timestamp
- Optional manager ID (for future multi-user support)

---

## 🤖 AI Model Integration

### Ollama Setup
```python
# Model: Llama 3.2:3b (can be upgraded to 13b)
# Connection: HTTP to http://localhost:11434
# Response: JSON with change detection

import ollama

response = ollama.generate(
    model="llama2",
    prompt=user_prompt,
    system=system_prompt,
    stream=False
)

# Expected response format:
# {"change_detected": true, "item": "X", "new_val": Y, "quote": "..."}
```

### System Prompt
```
You are a Tax Auditor. I will provide current database values and 
a new document text. If the tax percentage for an item has changed, 
return JSON: { "change_detected": true, "item": "name", 
"new_val": 12.0, "quote": "exact text from doc" }. 
If no change, return: { "change_detected": false }
```

---

## 🏗️ Backend Architecture

### Core Modules

#### 1. core/db.py - Database Connection
```python
# Singleton MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["lexaudit_flow"]

# Collections
tax_schemes = db["tax_schemes"]
pending_updates = db["pending_updates"]
audit_logs = db["audit_logs"]

# Functions
init_db()        # Create indexes
seed_database()  # Insert sample data
```

#### 2. core/models.py - Data Models
```python
# Pydantic models for validation
class TaxScheme(BaseModel): ...
class PendingUpdate(BaseModel): ...
class AuditLog(BaseModel): ...

# API models
class UpdateResponse(BaseModel): ...
class AnalysisResult(BaseModel): ...
```

#### 3. agents/crawler.py - Web Scraping
```python
async def crawl_and_download(url: str) -> list[str]:
    # Uses Playwright in headless mode
    # Rotates user-agents with fake-useragent
    # Returns list of downloaded PDF paths
    
    keywords = ["tax", "amendment", "scheme", ...]
    # Only downloads PDFs with these keywords
```

#### 4. agents/analyzer.py - AI Analysis
```python
def analyze_document(pdf_path: str) -> AnalysisResult:
    # Extract text from PDF
    # Send to Ollama with system prompt
    # Parse JSON response
    # Store in pending_updates if change detected
    
def store_pending_update(...):
    # Create pending_updates record
    # Link to evidence PDF
```

#### 5. agents/highlighter.py - PDF Annotation
```python
def generate_proof(pdf_path: str, quote_text: str) -> str:
    # Open original PDF with PyMuPDF
    # Search for quote text
    # Add yellow highlight annotation
    # Save to backend/evidence/highlighted/
    # Return path to highlighted PDF
```

#### 6. main.py - FastAPI Application
```python
# Endpoints
GET /tax-schemes              # Fetch all tax items
GET /updates                  # Fetch pending updates
GET /updates/{id}             # Get specific update
POST /updates/{id}/accept     # Accept/reject (CRITICAL)
GET /evidence/{filename}      # Serve PDFs
POST /crawl?url=X             # Trigger crawl
GET /audit-logs               # Fetch audit trail

# Middleware
CORSMiddleware               # Allow frontend requests
```

---

## 🎨 Frontend Architecture

### Component Hierarchy

```
App.jsx
├── Dashboard.jsx
│   ├── NotificationBadge.jsx (overlay)
│   ├── Left Panel
│   │   └── Update List (cards)
│   └── Right Panel
│       ├── Update Details
│       └── PDFViewer.jsx
└── Crawl Modal (conditional)
```

### Key Components

#### 1. Dashboard.jsx
- Main component managing app state
- Fetches updates every 30 seconds (polling)
- Handles accept/reject actions
- Manages selected update state

```javascript
const [updates, setUpdates] = useState([])
const [selectedUpdate, setSelectedUpdate] = useState(null)
const [notificationCount, setNotificationCount] = useState(0)

useEffect(() => {
  fetchUpdates()
  const interval = setInterval(fetchUpdates, 30000)
  return () => clearInterval(interval)
}, [])
```

#### 2. PDFViewer.jsx
- Displays PDF in iframe
- Shows accept/reject buttons
- Handles loading state

```javascript
<iframe src={pdfPath} />
<button onClick={onAccept}>Accept</button>
<button onClick={onReject}>Reject</button>
```

#### 3. NotificationBadge.jsx
- Floating notification showing pending count
- Appears when count > 0
- Uses lucide-react Bell icon

#### 4. api.js
- Axios HTTP client
- All API calls centralized
- Error handling and logging

---

## 🔄 Data Flow Diagrams

### Update Approval Flow
```
Manager Reviews → Clicks Accept → Frontend POST /accept
                                      │
                                      ▼
                            Backend Processes
                                      │
                    ┌──────────────┬──┴──┬──────────────┐
                    ▼              ▼     ▼              ▼
              Update DB      Mark Accepted  Log Action  Refresh UI
                    │              │        │           │
                    └──────────────┴────────┴───────────┘
                                    │
                                    ▼
                          Frontend Shows Success
```

### Evidence PDF Generation
```
PDF Downloaded → Extract Text → Analyze with Ollama
                                      │
                                      ▼
                            Change Detected?
                              /          \
                         Yes /            \ No
                           /                \
                          ▼                  ▼
                   Generate Proof      Skip Highlighting
                          │
                          ▼
                   Add Highlights
                          │
                          ▼
                   Save to /highlighted/
                          │
                          ▼
                   Store path in DB
```

---

## 🚀 Scalability Considerations

### Current Limitations
- Single-threaded PDF crawling (sequential)
- Synchronous Ollama calls
- No rate limiting
- In-memory update notifications

### Future Improvements
1. **Async Processing**: Use Celery + Redis for background jobs
2. **Rate Limiting**: Implement Redis-based rate limiting
3. **Batch Crawling**: Queue multiple URLs, process in parallel
4. **WebSocket**: Replace polling with real-time updates
5. **Multi-User**: Add user authentication and manager IDs
6. **Caching**: Redis for frequently accessed data

---

## 🔧 Configuration Reference

### Environment Variables (to add)
```
# .env file (create in project root)
MONGO_URI=mongodb://localhost:27017
DB_NAME=lexaudit_flow
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

### Key Settings Files

**backend/core/db.py**
- MongoDB connection string
- Database name

**backend/agents/analyzer.py**
- Ollama model name
- Ollama base URL
- System prompt

**backend/main.py**
- CORS origins
- API host/port

**frontend/src/api.js**
- Backend API URL
- Request timeout

---

## 🧪 Testing Strategy

### Unit Tests (to implement)
```python
# backend/tests/test_analyzer.py
def test_analyze_valid_pdf():
    result = analyze_document("test.pdf")
    assert result.change_detected == True

# backend/tests/test_crawler.py
def test_crawl_finds_pdfs():
    files = crawl_and_download("http://example.com")
    assert len(files) > 0
```

### Integration Tests (to implement)
```python
# Test full workflow
def test_crawl_analyze_approve_workflow():
    # 1. Crawl website
    # 2. Verify pending_updates created
    # 3. Accept update
    # 4. Verify tax_schemes updated
    # 5. Verify audit_logs recorded
```

### API Tests (to implement)
```javascript
// frontend/tests/api.test.js
test('GET /updates returns pending updates', async () => {
    const data = await getPendingUpdates()
    expect(data).toBeInstanceOf(Array)
})
```

---

## 📋 Deployment Checklist

Before deploying to production:

- [ ] Add environment variables
- [ ] Add user authentication
- [ ] Implement rate limiting
- [ ] Add error monitoring (Sentry)
- [ ] Add request logging
- [ ] Database backups enabled
- [ ] HTTPS/SSL configured
- [ ] CORS properly restricted
- [ ] Input validation hardened
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Load testing completed

---

## 📚 Related Documents

- README.md - Project overview
- SETUP_GUIDE.md - Installation instructions
- API_DOCUMENTATION.md - API endpoint reference
- This file (ARCHITECTURE.md) - System design

---

**Architecture Version**: 1.0
**Last Updated**: 2024-01-01
