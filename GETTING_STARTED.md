# LexAudit Flow - Getting Started Checklist ✅

## 🎯 Pre-Installation Checklist

### System Requirements
- [ ] **Windows 10/11** or Linux/macOS
- [ ] **Python 3.10+** installed
  - Verify: `python --version`
- [ ] **Node.js 18+** installed  
  - Verify: `node --version`
- [ ] **MongoDB** installed & accessible
  - Verify: `mongosh` connects to localhost:27017
- [ ] **Ollama** installed & Llama model downloaded
  - Verify: `ollama list` shows llama2 model

---

## 🚀 Installation Steps (In Order)

### Phase 1: Backend Setup (20 minutes)

```powershell
# Step 1: Navigate to backend
cd E:\dharmananda\LexAudit_Flow\backend

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Install Playwright browsers (5-10 min, runs once)
playwright install

# ✅ Backend setup complete!
```

**Success indicators:**
- All packages installed without errors
- No red text in output
- `pip list` shows installed packages

---

### Phase 2: Frontend Setup (5 minutes)

```powershell
# Step 1: Navigate to frontend (in new PowerShell window)
cd E:\dharmananda\LexAudit_Flow\frontend

# Step 2: Install dependencies
npm install

# ✅ Frontend setup complete!
```

**Success indicators:**
- No errors during npm install
- node_modules folder created
- All dependencies listed in package.json

---

## 🔧 Starting Services (4 terminals needed)

### Terminal 1: MongoDB
```powershell
# Run this in PowerShell
mongosh

# Expected output:
# Current Mongosh Log ID: ...
# test> 
# ✅ MongoDB is running
```

### Terminal 2: Ollama
```powershell
# Run this in PowerShell
ollama serve

# Expected output:
# time=... level=INFO msg="Listening on 127.0.0.1:11434 (version ...)"
# ✅ Ollama is running
```

### Terminal 3: Backend
```powershell
# Navigate to backend directory
cd E:\dharmananda\LexAudit_Flow\backend

# Activate venv if not already
.\venv\Scripts\Activate.ps1

# Run backend
python main.py

# Expected output:
# INFO:     Started server process [...]
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
# ✅ Backend is running
```

### Terminal 4: Frontend
```powershell
# Navigate to frontend directory
cd E:\dharmananda\LexAudit_Flow\frontend

# Run development server
npm run dev

# Expected output:
#   VITE v5.0.8  ready in XXX ms
#   ➜  Local:   http://localhost:5173/
# ✅ Frontend is running
```

---

## ✅ Verification Steps

Once all services are running, verify each:

### 1. Health Check
```powershell
# In any PowerShell window
Invoke-WebRequest -Uri "http://localhost:8000/" | ConvertTo-Json

# Expected: Status 200 OK
```

### 2. Check MongoDB Connection
```powershell
# In mongodb terminal
use lexaudit_flow
db.tax_schemes.find()

# Expected: Shows sample tax items
```

### 3. Check Ollama Connection
```powershell
# In any PowerShell window
Invoke-WebRequest -Uri "http://localhost:11434/" 

# Expected: Status 200 OK (might show "404" text but 200 status)
```

### 4. Open Dashboard
- Open browser: **http://localhost:5173**
- Should see: **LexAudit Flow** dashboard
- Should show: **Tax Change Alerts** section with items

---

## 🎯 First Test (Manual Workflow)

Once everything is running:

### 1. View Tax Schemes
- Dashboard loads
- Left panel shows "Tax Change Alerts: 0 pending"
- Sample data exists in database

### 2. Try Manual Crawl (Optional)
- Click "Crawl Website" button
- Enter a test URL
- Wait 30-60 seconds
- Observe backend logs for progress

### 3. Create Test Update (Skip crawl, test approval)
```powershell
# In MongoDB terminal (mongosh)
use lexaudit_flow

# Manually insert a test update
db.pending_updates.insertOne({
  detected_item: "Mobile Phones",
  current_db_val: 18.0,
  new_web_val: 20.0,
  evidence_pdf_path: "test_evidence.pdf",
  evidence_quote: "Tax rate increased to 20%",
  status: "pending",
  created_at: new Date(),
  updated_at: new Date()
})
```

### 4. Refresh Dashboard
- Close and reopen dashboard
- Should see new pending update
- Click to view (won't have PDF, but can test approval)

### 5. Test Approval
- Click "Accept Update"
- Check tax_schemes in MongoDB - should be updated
- Check audit_logs - should have record

---

## 🐛 Troubleshooting During Setup

| Error | Solution |
|-------|----------|
| `Connection refused` (MongoDB) | Run `mongosh` first |
| `Connection refused` (Ollama) | Run `ollama serve` first |
| `ModuleNotFoundError` (Python) | Run `pip install -r requirements.txt` |
| `npm not found` | Install Node.js from nodejs.org |
| Port 8000 already in use | Kill process: `netstat -ano \| findstr :8000` |
| CORS errors | Ensure all services on correct ports |

See **TROUBLESHOOTING.md** for more detailed solutions.

---

## 📁 File Structure Verification

After setup, you should have:

```
LexAudit_Flow/
├── backend/
│   ├── venv/              ✅ Virtual environment
│   ├── agents/
│   ├── core/
│   ├── evidence/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── node_modules/      ✅ Dependencies installed
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── README.md
├── SETUP_GUIDE.md
├── API_DOCUMENTATION.md
├── ARCHITECTURE.md
├── TROUBLESHOOTING.md
└── PROJECT_SUMMARY.md
```

---

## 🎓 Next: Understanding the System

After successful setup:

1. **Read ARCHITECTURE.md** to understand data flows
2. **Read API_DOCUMENTATION.md** to understand endpoints
3. **Explore backend/main.py** to see implemented routes
4. **Explore frontend/src/components/Dashboard.jsx** to understand UI
5. **Try modifying sample tax data** in MongoDB
6. **Test approval/rejection workflow** manually

---

## 🚀 Ready to Extend

Once verified, you can:

1. **Add custom tax websites** to crawl
2. **Modify AI prompts** in analyzer.py for better accuracy
3. **Add more tax items** to MongoDB
4. **Enhance dashboard UI** with more features
5. **Deploy to production** (add auth, security, etc.)

---

## 💡 Key Points to Remember

✅ **AI Analysis**
- Analyzer.py only proposes changes
- Cannot modify database directly
- Changes stored in pending_updates

✅ **Human Approval**
- Manager must review each update
- Must see highlighted PDF evidence
- Only approval changes the database

✅ **Audit Trail**
- Every decision is logged
- With timestamp and old/new values
- Complete audit history in audit_logs

✅ **Three Services Required**
- MongoDB (database)
- Ollama (AI model)
- FastAPI (backend) + React (frontend)

---

## 📞 Getting Help

If something doesn't work:

1. **Check TROUBLESHOOTING.md** first (20+ solutions)
2. **Verify all services are running** (4 terminals active)
3. **Check backend logs** for error messages
4. **Check browser console** (F12) for frontend errors
5. **Verify MongoDB connection** with `mongosh`

---

## ✨ Common Next Questions

**Q: Can I change the AI model?**
A: Yes, edit `backend/agents/analyzer.py` OLLAMA_MODEL

**Q: Can I use a different database?**
A: Yes, edit `backend/core/db.py` MONGO_URI

**Q: Can I change the ports?**
A: Yes, edit respective config files

**Q: How do I add more tax items?**
A: Insert into tax_schemes collection in MongoDB

**Q: How do I see API documentation?**
A: Run `python main.py` then visit http://localhost:8000/docs

---

## 📊 Expected Performance

| Task | Time |
|------|------|
| Python setup | 10-15 min (Playwright download) |
| Node setup | 2-3 min |
| First dashboard load | 2-3 sec |
| Tax schemes fetch | <1 sec |
| Crawl small website | 20-30 sec |
| Analyze one PDF | 5-10 sec |
| Update approval | <2 sec |

---

## 🎉 Success Criteria

Your setup is complete when:

- [ ] All 4 services start without errors
- [ ] MongoDB shows sample data with `db.tax_schemes.find()`
- [ ] Backend responds to `http://localhost:8000/`
- [ ] Frontend loads at `http://localhost:5173`
- [ ] Dashboard shows "Tax Change Alerts"
- [ ] Can trigger crawl (or manually insert test data)
- [ ] Can approve/reject updates
- [ ] Audit logs record decisions

---

## 🚦 Status Check Command

Run this to verify everything is set up:

```powershell
Write-Host "Checking LexAudit Flow Setup..." -ForegroundColor Cyan

# Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python installed" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found" -ForegroundColor Red
}

# Node
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✅ Node.js installed" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
}

# MongoDB
try {
    mongosh --eval "quit()" 2>$null
    Write-Host "✅ MongoDB available" -ForegroundColor Green
} catch {
    Write-Host "❌ MongoDB not available" -ForegroundColor Red
}

# Ollama
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "✅ Ollama installed" -ForegroundColor Green
} else {
    Write-Host "❌ Ollama not found" -ForegroundColor Red
}

# Backend setup
if (Test-Path "backend\venv") {
    Write-Host "✅ Backend venv exists" -ForegroundColor Green
} else {
    Write-Host "❌ Backend venv missing - run setup" -ForegroundColor Yellow
}

# Frontend setup
if (Test-Path "frontend\node_modules") {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend dependencies missing - run npm install" -ForegroundColor Yellow
}
```

---

## 📚 Documentation Reading Order

1. **This file** (Getting Started Checklist) - Current location
2. **README.md** - Project overview
3. **SETUP_GUIDE.md** - Detailed installation
4. **PROJECT_SUMMARY.md** - Quick reference
5. **ARCHITECTURE.md** - System design
6. **API_DOCUMENTATION.md** - API reference
7. **TROUBLESHOOTING.md** - Problem solving

---

## 🎯 You're All Set!

Everything is installed and configured. Now:

1. **Start all services** (follow instructions above)
2. **Open dashboard** at http://localhost:5173
3. **Test the workflow** (crawl or manually insert data)
4. **Review results** in dashboard
5. **Approve/reject** updates
6. **Check audit logs** to verify

---

**Last Updated**: January 1, 2024
**Status**: ✅ Ready to Go!

**Time to First Run**: ~30 minutes (including downloads)
**Maintenance**: Minimal - just keep services running

🚀 **Happy auditing!**
