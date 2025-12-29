# LexAudit Flow - Project Summary

## 📋 Quick Reference

### What is LexAudit Flow?
A **local, automated regulatory intelligence system** that:
1. Crawls government websites for tax policy changes
2. Analyzes PDFs using AI (Llama 3.2 via Ollama)
3. Proposes changes to a human manager
4. Requires manager approval before updating the database
5. Maintains complete audit trail of all decisions

### Key Principle: **Human-in-the-Loop**
```
AI Detects Change → Manager Reviews with Evidence → Manager Approves → Update Database
```

---

## 🚀 Quick Start (5 minutes)

### Prerequisites (install once)
```powershell
# 1. MongoDB - https://www.mongodb.com/try/download/community
# 2. Ollama - https://ollama.ai
# 3. Python 3.10+ - https://www.python.org
# 4. Node.js 18+ - https://nodejs.org
```

### Start Services
```powershell
# Terminal 1 - MongoDB (usually auto-runs)
mongosh

# Terminal 2 - Ollama
ollama serve

# Terminal 3 - Backend
cd backend
venv\Scripts\Activate.ps1
python main.py

# Terminal 4 - Frontend  
cd frontend
npm run dev
```

### Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📁 Project Structure

```
LexAudit_Flow/
├── backend/
│   ├── agents/
│   │   ├── crawler.py       # Playwright web scraper
│   │   ├── analyzer.py      # Llama AI analysis
│   │   └── highlighter.py   # PDF annotation
│   ├── core/
│   │   ├── db.py            # MongoDB connection
│   │   └── models.py        # Data models
│   ├── evidence/
│   │   ├── raw/             # Downloaded PDFs
│   │   └── highlighted/     # With evidence markers
│   ├── main.py              # FastAPI server
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── api.js           # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── README.md                # Overview
├── SETUP_GUIDE.md          # Installation details
├── API_DOCUMENTATION.md    # Endpoint reference
├── ARCHITECTURE.md         # System design
├── TROUBLESHOOTING.md      # Problem solving
└── quickstart.ps1          # Auto-start script
```

---

## 🔑 Key Features

### ✅ Automated Web Crawling
- Stealth crawling with fake user-agents
- Finds tax-related PDFs automatically
- Respects website rules

### ✅ AI Analysis
- Local Llama 3.2 model (no cloud)
- Detects tax percentage changes
- Highlights evidence in PDFs

### ✅ Manager Dashboard
- Side-by-side update list and evidence viewer
- Visual highlighting of detected changes
- One-click approve/reject

### ✅ Complete Audit Trail
- Every decision logged
- Timestamp + old/new values
- No hidden changes

### ✅ Database Safety
- AI cannot modify database
- Manager approval required
- Read-only AI analysis

---

## 📊 Data Model

### Three Collections (MongoDB)

**tax_schemes** - What we know now
```javascript
{item_name: "Mobile Phones", tax_percentage: 18.0}
```

**pending_updates** - AI recommendations waiting for approval
```javascript
{
  detected_item: "Mobile Phones",
  current_db_val: 18.0,
  new_web_val: 20.0,
  status: "pending"
}
```

**audit_logs** - Complete decision history
```javascript
{
  action: "update_accepted",
  item_name: "Mobile Phones",
  old_value: 18.0,
  new_value: 20.0
}
```

---

## 🔄 Typical Workflow

### Step 1: Crawl
```
Manager enters URL → Backend crawls website → Downloads PDFs
```

### Step 2: Analyze
```
For each PDF → Extract text → Send to Ollama → Get JSON response
```

### Step 3: Propose
```
If change detected → Create pending_update → Wait for approval
```

### Step 4: Review
```
Manager sees alert → Views highlighted PDF → Reads evidence quote
```

### Step 5: Approve/Reject
```
Manager clicks button → Backend updates database → Logs action
```

---

## 🛡️ Safety Constraints

1. **AI Read-Only Analysis**
   - Analyzer cannot modify database
   - Only proposes changes

2. **Mandatory Human Review**
   - Every change needs approval
   - Must see evidence PDF

3. **Audit Everything**
   - Timestamp every decision
   - Log old and new values

4. **Limited Scope**
   - Only 2 fields can change: item_name, tax_percentage
   - No bulk operations without approval

---

## 📱 Frontend Components

| Component | Purpose |
|-----------|---------|
| Dashboard | Main view with list + PDF viewer |
| Update Cards | Click to select pending update |
| PDFViewer | Shows highlighted evidence |
| NotificationBadge | Alerts when new updates arrive |

---

## ⚙️ Backend Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/tax-schemes` | Get all tax items |
| GET | `/updates` | Get pending updates |
| POST | `/updates/{id}/accept` | **Approve/reject change** |
| GET | `/evidence/{filename}` | Download PDF |
| POST | `/crawl?url=X` | Start crawl job |
| GET | `/audit-logs` | View decisions |

---

## 🧠 AI System

**Model**: Llama 3.2:3b (can upgrade to 13b for accuracy)
**Connection**: Local via Ollama HTTP API
**Prompt**: Structured to return JSON with change detection
**Response**: `{change_detected, item, new_val, quote}`

---

## 🔧 Configuration Files

| File | Purpose | Key Settings |
|------|---------|--------------|
| `backend/core/db.py` | MongoDB connection | MONGO_URI, DB_NAME |
| `backend/agents/analyzer.py` | Ollama settings | OLLAMA_MODEL, OLLAMA_BASE_URL |
| `backend/main.py` | FastAPI config | CORS origins, port |
| `frontend/src/api.js` | Backend URL | API_BASE_URL |

---

## 🚨 Common Issues Quick Fixes

| Issue | Fix |
|-------|-----|
| MongoDB connection error | Run `mongosh` to verify connection |
| Ollama connection error | Run `ollama serve` in separate terminal |
| CORS error | Ensure backend on 8000, frontend on 5173 |
| No updates after crawl | Check Ollama is running, check PDF keywords |
| Port already in use | Kill process on port or change port |

See **TROUBLESHOOTING.md** for detailed debugging.

---

## 📈 Performance Notes

| Task | Time |
|------|------|
| Crawl small website | 10-20 seconds |
| Analyze one PDF | 5-15 seconds |
| Full crawl + analysis | 30-60 seconds |
| API response | <100ms |
| Dashboard load | <500ms |

---

## 🔐 Security Considerations

✅ **Already Implemented**
- CORS enabled for localhost
- MongoDB indexes for performance
- Audit logging for all decisions
- AI cannot modify database

⚠️ **To Add for Production**
- User authentication
- Rate limiting
- HTTPS/SSL
- API key authentication
- Input sanitization
- Error monitoring (Sentry)

---

## 🎓 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + Vite | User interface |
| Styling | Tailwind CSS | Design system |
| Backend | FastAPI | REST API |
| Database | MongoDB | Data storage |
| AI | Llama 3.2 + Ollama | Analysis engine |
| Crawling | Playwright + Python | Web scraping |
| PDF | PyMuPDF | Highlighting |

---

## 📚 Documentation

1. **README.md** - Project overview & features
2. **SETUP_GUIDE.md** - Step-by-step installation
3. **API_DOCUMENTATION.md** - Full API reference
4. **ARCHITECTURE.md** - System design & diagrams
5. **TROUBLESHOOTING.md** - Problem solving guide
6. **PROJECT_SUMMARY.md** - This file

---

## 🎯 Success Criteria

Your setup is complete when:

- ✅ All services start without errors
- ✅ Dashboard loads at localhost:5173
- ✅ Tax schemes display (auto-seeded sample data)
- ✅ Can trigger crawl and see results
- ✅ Can approve/reject updates
- ✅ Audit logs record all decisions

---

## 🚀 Next Steps

1. **Follow SETUP_GUIDE.md** for installation
2. **Run sample workflow** to verify system works
3. **Configure real tax websites** to crawl
4. **Fine-tune AI prompts** for accuracy
5. **Add user authentication** for production
6. **Set up monitoring** and backups

---

## 📞 Support

- **Setup Issues**: See SETUP_GUIDE.md & TROUBLESHOOTING.md
- **API Issues**: See API_DOCUMENTATION.md
- **Architecture Questions**: See ARCHITECTURE.md
- **Code Issues**: Check inline comments in Python/React files

---

## 🎉 You're Ready!

Everything is scaffolded. Time to:
1. Install prerequisites
2. Run setup guide
3. Start all services
4. Access dashboard at localhost:5173

**Happy auditing!** 🚀

---

**Project Version**: 1.0.0
**Last Updated**: January 1, 2024
**Status**: ✅ Ready for Development
