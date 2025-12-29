# LexAudit Flow - Troubleshooting Guide

## 🔍 Common Issues & Solutions

### ❌ MongoDB Connection Error

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError: 
localhost:27017: [Errno 111] Connection refused
```

**Causes & Solutions:**

1. **MongoDB not running**
   ```powershell
   # Check if MongoDB is running
   mongosh
   # Should connect without error
   ```

2. **Wrong connection string**
   - Verify in `backend/core/db.py`
   - Default: `mongodb://localhost:27017`
   - For Atlas: use connection string from MongoDB dashboard

3. **Port blocked**
   ```powershell
   # Check if port 27017 is in use
   Get-NetTCPConnection -LocalPort 27017
   ```

4. **MongoDB not installed**
   - Download from: https://www.mongodb.com/try/download/community
   - Follow OS-specific installation guide

**Fix:**
```powershell
# Windows - Start MongoDB
# Usually auto-starts as service, check Services app

# Manual start (if installed manually):
mongod.exe
```

---

### ❌ Ollama Connection Error

**Error:**
```
HTTPConnectionPool(host='localhost', port=11434): 
Max retries exceeded with url: /api/generate
```

**Causes & Solutions:**

1. **Ollama not running**
   ```powershell
   ollama serve
   # Should start server on http://localhost:11434
   ```

2. **Wrong port**
   - Verify in `backend/agents/analyzer.py`
   - Default: `http://localhost:11434`

3. **Model not downloaded**
   ```powershell
   ollama pull llama2
   # Wait for download to complete (~5GB)
   ```

4. **Ollama not installed**
   - Download from: https://ollama.ai
   - Follow installation instructions

**Fix:**
```powershell
# Start Ollama
ollama serve

# In another terminal, verify:
Invoke-WebRequest -Uri "http://localhost:11434"
```

---

### ❌ Playwright Browser Not Installed

**Error:**
```
playwright._impl._errors.Error: 
Executable doesn't exist at .../chromium-...
```

**Solution:**
```powershell
cd backend
playwright install
# Wait for downloads to complete
```

---

### ❌ FastAPI Fails to Start

**Error:**
```
Address already in use
```

**Causes & Solutions:**

1. **Port 8000 already in use**
   ```powershell
   # Find process using port 8000
   Get-NetTCPConnection -LocalPort 8000
   
   # Kill the process
   Stop-Process -Id <PID> -Force
   ```

2. **Backend already running**
   - Check if another terminal has backend running
   - Close that terminal or press Ctrl+C

3. **Change port in code**
   ```python
   # In backend/main.py, change:
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```

---

### ❌ Frontend Cannot Connect to Backend

**Error:**
```
CORS policy: No 'Access-Control-Allow-Origin' header
```

**Causes & Solutions:**

1. **Backend not running**
   ```powershell
   # Verify backend is running
   Invoke-WebRequest -Uri "http://localhost:8000"
   # Should succeed
   ```

2. **CORS not configured**
   - Already configured in `backend/main.py`
   - Allows: `http://localhost:5173`, `http://localhost:3000`, `*`

3. **Wrong backend URL**
   - Check `frontend/src/api.js`
   - Should be: `http://localhost:8000`

**Fix:**
```javascript
// In frontend/src/api.js
const API_BASE_URL = 'http://localhost:8000';
```

---

### ❌ Node Dependencies Error

**Error:**
```
npm ERR! Cannot read properties of undefined (reading 'forEach')
```

**Solution:**
```powershell
cd frontend

# Clear cache and reinstall
rm -r node_modules package-lock.json
npm install
```

---

### ❌ Python Virtual Environment Not Activating

**Error:**
```
The file venv\Scripts\Activate.ps1 is not digitally signed
```

**Solution:**
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

---

### ❌ PDF Highlighting Not Working

**Error:**
```
quote_text not found in PDF
```

**Causes & Solutions:**

1. **Quote text doesn't match exactly**
   - Whitespace/formatting differences
   - Special characters not captured
   - Text split across pages

2. **PDF is image-based (scanned)**
   - Requires OCR processing
   - Current system only handles text PDFs
   - Try converting PDF with OCR first

3. **PyMuPDF version issue**
   ```powershell
   pip install --upgrade PyMuPDF
   ```

**Debug:**
```python
# In backend/agents/analyzer.py
import fitz

doc = fitz.open("test.pdf")
page = doc[0]
text = page.get_text()
print(text)  # See what text is actually in PDF
```

---

### ❌ No Updates Appearing After Crawl

**Checklist:**

1. **Check Ollama is responding**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:11434"
   # Should return 200 OK
   ```

2. **Check PDFs were downloaded**
   ```powershell
   dir backend\evidence\raw\
   # Should show PDF files
   ```

3. **Check backend logs**
   - Look for error messages in backend terminal
   - Search for "change_detected"

4. **Website has no tax PDFs**
   - Crawler looks for keywords: tax, amendment, scheme, regulation
   - If website doesn't contain these, no PDFs downloaded
   - Try a government tax website

5. **Crawl timed out**
   - Large websites take 10-60+ seconds
   - Check if crawl completed in backend logs

---

### ⚠️ Slow Performance

**Issue: Crawl taking too long**

**Causes:**
- Large website with many PDFs
- Network speed
- Ollama model is large (3.2:3b or 13b)

**Solutions:**
```python
# Reduce crawl depth (in agents/crawler.py)
MAX_PDF_COUNT = 10  # Limit PDFs downloaded

# Use faster Ollama model (if available)
OLLAMA_MODEL = "mistral"  # Faster than llama2
```

**Issue: Frontend is slow**

**Solutions:**
1. **Increase polling interval** (less API calls)
   ```javascript
   // In Dashboard.jsx
   const interval = setInterval(fetchUpdates, 60000)  // 60s instead of 30s
   ```

2. **Pagination for updates** (limit list size)
   ```javascript
   const PAGE_SIZE = 10
   const paginatedUpdates = updates.slice(0, PAGE_SIZE)
   ```

---

### 🔓 PDF Not Opening in Browser

**Error:**
```
Cannot open application for the file
```

**Causes:**

1. **Incorrect file path**
   - Path in database includes `backend/` prefix
   - Frontend should request: `/evidence/filename.pdf`
   - Backend serves from: `backend/evidence/highlighted/`

2. **PDF is corrupted**
   - Check if PDF opens locally
   - Try regenerating with highlighter

**Fix:**
```javascript
// In frontend, use getEvidenceFile helper
import { getEvidenceFile } from '../api'

const pdfUrl = getEvidenceFile(filename)
// Results in: http://localhost:8000/evidence/filename.pdf
```

---

### ❌ "Update Not Found" Error

**Error:**
```json
{"detail": "Update not found"}
```

**Causes:**

1. **Update already processed**
   - Update was already accepted/rejected
   - Refreshing page shows it gone
   - Expected behavior

2. **Wrong update ID**
   - Frontend using invalid ObjectId
   - Check browser console for ID

3. **Database issue**
   ```powershell
   mongosh
   use lexaudit_flow
   db.pending_updates.find({status: "pending"})
   # Verify updates exist
   ```

---

### ❌ Changes Not Saving

**Error:**
Accept button clicked but nothing happens

**Checklist:**

1. **Check browser console** (F12)
   - Look for network errors
   - Check if POST request is sent

2. **Verify backend is running**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:8000"
   ```

3. **Check MongoDB connection**
   ```powershell
   mongosh
   use lexaudit_flow
   db.tax_schemes.find()
   # Should show tax items
   ```

4. **Check if update exists**
   ```powershell
   mongosh
   use lexaudit_flow
   db.pending_updates.findOne({_id: ObjectId("...")})
   ```

---

### 📚 Database Schema Verification

Check if collections exist and have correct structure:

```powershell
mongosh
use lexaudit_flow

# Check tax_schemes
db.tax_schemes.find().pretty()

# Check pending_updates
db.pending_updates.find().pretty()

# Check audit_logs
db.audit_logs.find().pretty()

# Check indexes
db.tax_schemes.getIndexes()
db.pending_updates.getIndexes()
db.audit_logs.getIndexes()
```

---

## 🔧 Reset Database

**Warning**: This deletes all data!

```powershell
mongosh
use lexaudit_flow

# Drop all collections
db.tax_schemes.deleteMany({})
db.pending_updates.deleteMany({})
db.audit_logs.deleteMany({})

# Or drop entire database
db.dropDatabase()
```

Then restart backend (will reseed with sample data):
```powershell
python main.py
# Will auto-initialize and seed database
```

---

## 🧹 Clean Installation

If something is severely broken:

```powershell
# 1. Stop all services (close terminals)

# 2. Reset database
mongosh
use lexaudit_flow
db.dropDatabase()

# 3. Clear Python cache
cd backend
rm -r __pycache__ -Recurse
rm -r */__pycache__ -Recurse
rm -r venv

# 4. Clear Node cache
cd ..\frontend
rm -r node_modules
rm package-lock.json

# 5. Reinstall everything
cd ..\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install

cd ..\frontend
npm install

# 6. Start fresh
# Terminal 1: mongosh
# Terminal 2: ollama serve
# Terminal 3: cd backend && python main.py
# Terminal 4: cd frontend && npm run dev
```

---

## 📊 Debug Utilities

### Check All Services Status

```powershell
$services = @(
    ("Backend", "http://localhost:8000/"),
    ("Frontend", "http://localhost:5173/"),
    ("Ollama", "http://localhost:11434/"),
    ("MongoDB", "mongodb://localhost:27017")
)

foreach ($service in $services) {
    $name, $url = $service
    try {
        if ($url -like "mongodb://*") {
            mongosh --eval "quit()" 2>$null
            Write-Host "✅ $name is running" -ForegroundColor Green
        } else {
            $response = Invoke-WebRequest -Uri $url -TimeoutSec 2
            Write-Host "✅ $name is running" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ $name is NOT running" -ForegroundColor Red
    }
}
```

### View Recent Logs

```powershell
# Backend logs (last 20 lines)
Get-Content backend.log -Tail 20

# API requests
curl -X GET http://localhost:8000/tax-schemes | ConvertFrom-Json | ConvertTo-Json
```

---

## 🚨 Emergency Contacts

- **Ollama Issues**: https://github.com/ollama/ollama/issues
- **MongoDB Issues**: https://docs.mongodb.com/manual/
- **FastAPI Issues**: https://fastapi.tiangolo.com
- **React/Vite Issues**: https://vitejs.dev

---

## 📝 Logging Configuration

Enable detailed logging for debugging:

```python
# In backend/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
```

---

**Last Updated**: 2024-01-01
**Version**: 1.0
