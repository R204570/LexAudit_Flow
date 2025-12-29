# LexAudit Flow - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required (development mode). CORS is enabled for frontend on localhost:5173.

---

## Endpoints

### 1. Health Check

#### GET `/`
Check if the backend is running.

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "LexAudit Flow Backend is running"
}
```

---

### 2. Tax Schemes Management

#### GET `/tax-schemes`
Fetch all tax schemes from the database.

**Response (200 OK):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "item_name": "Mobile Phones",
    "tax_percentage": 18.0,
    "last_updated": "2024-01-01T12:00:00"
  },
  {
    "_id": "507f1f77bcf86cd799439012",
    "item_name": "Laptops",
    "tax_percentage": 18.0,
    "last_updated": "2024-01-01T12:00:00"
  }
]
```

**Error (500):**
```json
{
  "detail": "Failed to fetch tax schemes"
}
```

---

### 3. Pending Updates Management

#### GET `/updates`
Fetch all pending updates (status = "pending").

**Response (200 OK):**
```json
[
  {
    "id": "507f1f77bcf86cd799439013",
    "detected_item": "Mobile Phones",
    "current_db_val": 18.0,
    "new_web_val": 20.0,
    "evidence_pdf_path": "backend/evidence/highlighted/507f1f77bcf86cd799439013_highlighted.pdf",
    "evidence_quote": "The tax rate for mobile phones has been increased to 20%",
    "status": "pending",
    "created_at": "2024-01-02T10:30:00"
  }
]
```

**Error (500):**
```json
{
  "detail": "Failed to fetch pending updates"
}
```

---

#### GET `/updates/{update_id}`
Get details of a specific update.

**Parameters:**
- `update_id` (path, required): MongoDB ObjectId of the update

**Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439013",
  "detected_item": "Mobile Phones",
  "current_db_val": 18.0,
  "new_web_val": 20.0,
  "evidence_pdf_path": "backend/evidence/highlighted/507f1f77bcf86cd799439013_highlighted.pdf",
  "evidence_quote": "The tax rate for mobile phones has been increased to 20%",
  "status": "pending",
  "created_at": "2024-01-02T10:30:00"
}
```

**Error (404):**
```json
{
  "detail": "Update not found"
}
```

**Error (500):**
```json
{
  "detail": "Failed to fetch update"
}
```

---

#### POST `/updates/{update_id}/accept`
Accept or reject a pending update. Only this endpoint can modify tax_schemes.

**Parameters:**
- `update_id` (path, required): MongoDB ObjectId of the update

**Request Body:**
```json
{
  "accept": true
}
```

**Response (200 OK) - Accept:**
```json
{
  "status": "accepted",
  "message": "Update accepted successfully"
}
```

**What happens when accepted:**
1. Updates `tax_schemes` collection with new tax_percentage
2. Marks update status as "accepted"
3. Logs action to `audit_logs` collection

**Response (200 OK) - Reject:**
```json
{
  "status": "rejected",
  "message": "Update rejected"
}
```

**What happens when rejected:**
1. Marks update status as "rejected"
2. Logs rejection to `audit_logs` collection
3. Does NOT modify tax_schemes

**Error (404):**
```json
{
  "detail": "Update not found"
}
```

**Error (500):**
```json
{
  "detail": "Failed to process update"
}
```

---

### 4. Evidence Files

#### GET `/evidence/{filename}`
Serve highlighted or raw PDF evidence files.

**Parameters:**
- `filename` (path, required): Name of the PDF file

**Response (200 OK):**
- Returns PDF file with Content-Type: application/pdf
- Can be embedded in iframe or opened in browser

**Error (404):**
```json
{
  "detail": "Evidence file not found"
}
```

**Example Usage in Frontend:**
```javascript
// In iframe
<iframe src="http://localhost:8000/evidence/507f1f77bcf86cd799439013_highlighted.pdf" />

// Or direct download
window.open('http://localhost:8000/evidence/highlighted_file.pdf')
```

---

### 5. Crawling & Analysis

#### POST `/crawl`
Trigger a website crawl and automatic analysis.

**Query Parameters:**
- `url` (required): Website URL to crawl

**Example:**
```
POST http://localhost:8000/crawl?url=https://tax.example.com
```

**Response (200 OK):**
```json
{
  "status": "completed",
  "downloaded_files": [
    "/path/to/backend/evidence/raw/tax_document_1.pdf",
    "/path/to/backend/evidence/raw/tax_amendment_2.pdf"
  ],
  "analysis_results": [
    {
      "pdf": "/path/to/backend/evidence/raw/tax_document_1.pdf",
      "change_detected": true,
      "item": "Mobile Phones",
      "new_val": 20.0
    },
    {
      "pdf": "/path/to/backend/evidence/raw/tax_amendment_2.pdf",
      "change_detected": false,
      "item": null,
      "new_val": null
    }
  ]
}
```

**What happens during crawl:**
1. Visits the URL with Playwright
2. Searches for PDF links with tax-related keywords
3. Downloads matching PDFs
4. Analyzes each PDF with Ollama/Llama
5. If change detected, creates pending_update record
6. Generates highlighted PDF with evidence

**Error (400):**
```json
{
  "detail": "URL is required"
}
```

**Error (500):**
```json
{
  "detail": "Crawl failed"
}
```

---

### 6. Audit Logs

#### GET `/audit-logs`
Fetch all recorded actions (accepts/rejects/updates).

**Response (200 OK):**
```json
[
  {
    "id": "507f1f77bcf86cd799439014",
    "action": "update_accepted",
    "item_name": "Mobile Phones",
    "old_value": 18.0,
    "new_value": 20.0,
    "timestamp": "2024-01-02T10:35:00"
  },
  {
    "id": "507f1f77bcf86cd799439015",
    "action": "update_rejected",
    "item_name": "Laptops",
    "old_value": 18.0,
    "new_value": 15.0,
    "timestamp": "2024-01-02T10:40:00"
  }
]
```

**Fields:**
- `action`: "update_accepted" or "update_rejected"
- `item_name`: Name of the tax item
- `old_value`: Previous tax percentage
- `new_value`: Proposed tax percentage
- `timestamp`: When the action was taken

**Error (500):**
```json
{
  "detail": "Failed to fetch audit logs"
}
```

---

## Request/Response Examples

### Example 1: Get Pending Updates and Accept One

```bash
# 1. Fetch pending updates
curl -X GET http://localhost:8000/updates

# Response:
# [
#   {
#     "id": "507f1f77bcf86cd799439013",
#     "detected_item": "Mobile Phones",
#     "current_db_val": 18.0,
#     "new_web_val": 20.0,
#     ...
#   }
# ]

# 2. Accept the update
curl -X POST http://localhost:8000/updates/507f1f77bcf86cd799439013/accept \
  -H "Content-Type: application/json" \
  -d '{"accept": true}'

# Response:
# {"status": "accepted", "message": "Update accepted successfully"}
```

### Example 2: Crawl a Website

```bash
curl -X POST "http://localhost:8000/crawl?url=https://tax.example.com"

# Response:
# {
#   "status": "completed",
#   "downloaded_files": [...],
#   "analysis_results": [...]
# }
```

### Example 3: Get Evidence PDF

```bash
# Download or view in browser
http://localhost:8000/evidence/507f1f77bcf86cd799439013_highlighted.pdf
```

---

## Error Handling

All errors return appropriate HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad Request (missing/invalid parameters) |
| 404 | Not Found (update/file doesn't exist) |
| 500 | Server Error (database/processing error) |

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting
Currently, no rate limiting is enforced. For production, implement:
- Redis-based rate limiting
- Crawl job queuing
- Request throttling

---

## Constraints & Business Rules

### Critical Rules
1. ✋ **AI Cannot Modify Database**: Only `/updates/{id}/accept` endpoint can update `tax_schemes`
2. ✋ **Only Two Fields Can Change**: `item_name` and `tax_percentage`
3. 📋 **Human Approval Required**: All changes must be reviewed and accepted by manager
4. 📝 **Complete Audit Trail**: Every action is logged with timestamp

### Data Validation
- `tax_percentage` must be a positive number (0-100)
- `item_name` must not be empty
- URLs must be valid HTTP/HTTPS

---

## Testing the API

### Using PowerShell

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/"

# Get tax schemes
(Invoke-WebRequest -Uri "http://localhost:8000/tax-schemes").Content | ConvertFrom-Json

# Get pending updates
(Invoke-WebRequest -Uri "http://localhost:8000/updates").Content | ConvertFrom-Json

# Accept an update
$body = @{ accept = $true } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/updates/{update_id}/accept" -Method POST -Body $body -ContentType "application/json"
```

### Using Python

```python
import requests

# Get pending updates
response = requests.get('http://localhost:8000/updates')
updates = response.json()

# Accept first update
if updates:
    update_id = updates[0]['id']
    response = requests.post(
        f'http://localhost:8000/updates/{update_id}/accept',
        json={'accept': True}
    )
    print(response.json())
```

### Using JavaScript/Fetch

```javascript
// Get pending updates
fetch('http://localhost:8000/updates')
  .then(r => r.json())
  .then(updates => console.log(updates))

// Accept an update
fetch('http://localhost:8000/updates/{update_id}/accept', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ accept: true })
})
  .then(r => r.json())
  .then(result => console.log(result))
```

---

## API Interaction Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    API Interaction Flow                       │
└──────────────────────────────────────────────────────────────┘

1. CRAWL TRIGGER
   Frontend → POST /crawl?url=X → Backend

2. PDF ANALYSIS
   Backend downloads PDFs
   Backend → Ollama (Local LLM) → Detects changes

3. PROPOSAL STORAGE
   Backend → MongoDB pending_updates collection

4. MANAGER REVIEW
   Frontend → GET /updates → Display in Dashboard
   Backend → GET /evidence/{filename} → Serve highlighted PDF

5. MANAGER DECISION
   Frontend → POST /updates/{id}/accept → Backend
   Backend → MongoDB tax_schemes (update)
   Backend → MongoDB audit_logs (record action)

6. AUDIT TRAIL
   Frontend → GET /audit-logs → Display history
```

---

## Performance Notes

- **Crawl Time**: Depends on website size and PDF count (typically 10-60 seconds)
- **Analysis Time**: Per PDF, ~5-15 seconds with Llama 3.2:3b
- **API Response Time**: <100ms for database queries, <500ms for crawls

---

**Last Updated**: 2024-01-01
**Version**: 1.0.0
