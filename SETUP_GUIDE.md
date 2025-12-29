# LexAudit Flow - Complete Setup Guide

## ✅ Prerequisites Check

Before starting, ensure you have:

- [x] MongoDB running locally on `mongodb://localhost:27017`
- [x] Ollama installed with Llama 3.2:3b model
- [x] Python 3.10 or higher
- [x] Node.js 18 or higher
- [x] Git installed

## 📦 Installation Steps

### Prerequisites Installation

#### 1. Install MongoDB
- Download from: https://www.mongodb.com/try/download/community
- Follow official installation guide for your OS
- Verify: `mongosh` in terminal should connect to local database

#### 2. Install Ollama
- Download from: https://ollama.ai
- Install following official instructions
- Download Llama model: `ollama pull llama2`
- Verify: `ollama serve` should start the service on http://localhost:11434

#### 3. Install Python (if needed)
- Download from: https://www.python.org/downloads/
- Ensure Python 3.10+ is installed
- Verify: `python --version`

#### 4. Install Node.js (if needed)
- Download from: https://nodejs.org/
- Ensure Node 18+ is installed
- Verify: `node --version`

---

### Backend Setup (Python)

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Create a virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows PowerShell:
venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Playwright browsers (one-time, takes a few minutes)
playwright install

# 6. Start the backend server
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Backend is ready when you see this message!

---

### Frontend Setup (React)

```powershell
# In a NEW TERMINAL/POWERSHELL, navigate to frontend
cd frontend

# 1. Install dependencies
npm install

# 2. Start development server
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

✅ Frontend is ready when you see this message!

---

## 🚀 First Run Verification

### 1. Check Backend Health
Open in browser: `http://localhost:8000`
You should see: `{"status": "ok", "message": "LexAudit Flow Backend is running"}`

### 2. Check API Endpoints
Try these endpoints in your browser or Postman:

- Health: `http://localhost:8000/`
- Tax Schemes: `http://localhost:8000/tax-schemes`
- Pending Updates: `http://localhost:8000/updates`
- Audit Logs: `http://localhost:8000/audit-logs`

### 3. Check Frontend
Open in browser: `http://localhost:5173`
You should see the LexAudit Flow Manager Dashboard

### 4. Verify Database Seeding
The backend automatically seeds sample data on startup. You should see:
- Mobile Phones: 18%
- Laptops: 18%
- Tablets: 12%
- Software: 18%

---

## 📋 Full Workflow Test

### Step 1: Start All Services

**Terminal 1 - MongoDB:**
```powershell
mongosh
# Should connect successfully
```

**Terminal 2 - Ollama:**
```powershell
ollama serve
```

**Terminal 3 - Backend:**
```powershell
cd backend
python main.py
```

**Terminal 4 - Frontend:**
```powershell
cd frontend
npm run dev
```

### Step 2: Test Manual Crawl

1. Go to `http://localhost:5173`
2. Click "Crawl Website" button
3. Enter a test URL (e.g., a website with tax PDFs)
4. The system will:
   - Crawl the website
   - Download PDFs
   - Analyze with Ollama
   - Show results in dashboard

### Step 3: Test Manager Approval

1. After crawl completes, check the dashboard
2. Click on a pending update in the left panel
3. Review the highlighted PDF in the right panel
4. Click "Accept" or "Reject"
5. Check audit logs to verify the action was recorded

---

## 🔧 Configuration Reference

### Backend Configuration

**`backend/core/db.py`** - MongoDB Connection
```python
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lexaudit_flow"
```

**`backend/agents/analyzer.py`** - Ollama Model
```python
OLLAMA_MODEL = "llama2"  # Change to llama2:13b for better accuracy
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Frontend Configuration

**`frontend/src/api.js`** - Backend API URL
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

---

## 📊 Database Schema Overview

### Collections Created Automatically

1. **tax_schemes** - Source of truth for tax rates
   ```json
   {
     "item_name": "Mobile Phones",
     "tax_percentage": 18.0,
     "last_updated": "2024-01-01T00:00:00Z"
   }
   ```

2. **pending_updates** - AI recommendations
   ```json
   {
     "detected_item": "Mobile Phones",
     "current_db_val": 18.0,
     "new_web_val": 20.0,
     "evidence_pdf_path": "/path/highlighted.pdf",
     "evidence_quote": "...change text...",
     "status": "pending"
   }
   ```

3. **audit_logs** - Complete action history
   ```json
   {
     "action": "update_accepted",
     "item_name": "Mobile Phones",
     "old_value": 18.0,
     "new_value": 20.0,
     "timestamp": "2024-01-01T00:00:00Z"
   }
   ```

---

## 🐛 Troubleshooting

### Issue: Backend won't start - "Connection refused"
**Solution:** Ensure MongoDB is running
```powershell
mongosh  # Should connect without errors
```

### Issue: "Ollama not running" error
**Solution:** Start Ollama in a separate terminal
```powershell
ollama serve
```

### Issue: Playwright browser download fails
**Solution:** Ensure you ran `playwright install`
```powershell
cd backend
playwright install
```

### Issue: Frontend shows CORS error
**Solution:** Ensure both backend and frontend are running:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### Issue: No updates appear after crawl
**Possible causes:**
1. Crawled website has no tax-related PDFs
2. Ollama is not responding (check `ollama serve`)
3. PDF text doesn't match model's expectations
4. Check backend logs for detailed error messages

---

## 📝 Development Tips

### Running with Debug Logging

**Backend:**
```powershell
# Edit main.py and change logging level
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```powershell
# Check browser console for React/Axios logs
```

### Database Operations

View data in MongoDB:
```powershell
mongosh
use lexaudit_flow
db.tax_schemes.find()
db.pending_updates.find()
db.audit_logs.find()
```

### API Testing with PowerShell

```powershell
# Get pending updates
Invoke-WebRequest -Uri "http://localhost:8000/updates"

# Trigger crawl
Invoke-WebRequest -Uri "http://localhost:8000/crawl?url=https://example.com" -Method POST
```

---

## 🎯 Next Steps

1. ✅ Complete setup
2. ✅ Test with sample data
3. 📚 Customize tax items in database
4. 🌐 Configure real government websites to crawl
5. 🤖 Fine-tune Ollama prompts for better accuracy
6. 📊 Integrate with your existing systems

---

## 📚 Documentation Structure

- **README.md** - Project overview and quick start
- **SETUP_GUIDE.md** - This file, detailed setup instructions
- **API_DOCUMENTATION.md** - Full API endpoint reference
- **Backend Code** - Inline comments in Python files
- **Frontend Components** - JSDoc comments in React files

---

## ✨ Success Indicators

Your setup is complete when:

- ✅ Backend starts without errors
- ✅ Frontend loads dashboard at localhost:5173
- ✅ Can fetch tax schemes via API
- ✅ Sample data is visible in dashboard
- ✅ Can accept/reject updates successfully
- ✅ Audit logs record all actions
- ✅ Can trigger crawls and see results

---

## 🆘 Getting Help

If you encounter issues:

1. Check backend logs for detailed error messages
2. Verify all services are running (MongoDB, Ollama, Backend, Frontend)
3. Check browser console for frontend errors
4. Review troubleshooting section above
5. Ensure all prerequisites are properly installed

---

**Happy auditing! 🎉**
