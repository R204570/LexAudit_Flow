# 🎯 DATABASE SETUP - STEP BY STEP VISUAL GUIDE

## ⏱️ Takes Only 5 Minutes!

---

## 📍 STEP 1: Open First PowerShell Terminal

```
Open PowerShell and type:
mongosh

You should see:
  Current Mongosh Log ID: ...
  test>  ← This means MongoDB is ready!
```

**✅ Keep this terminal OPEN**

---

## 📍 STEP 2: Open Second PowerShell Terminal

```
New PowerShell window
Navigate to project folder:

cd E:\dharmananda\LexAudit_Flow
```

---

## 📍 STEP 3: Run Database Setup Script

```powershell
.\setup_database.ps1
```

---

## 📍 STEP 4: Wait for Success Message

```
You'll see something like:

╔════════════════════════════════════════════════════════════════╗
║     LexAudit Flow - Database Initialization                    ║
╚════════════════════════════════════════════════════════════════╝

✅ Successfully connected to MongoDB
✅ Database 'lexaudit_flow' ready
✅ Created collection: tax_schemes
✅ Created collection: pending_updates
✅ Created collection: audit_logs
✅ Created collection: users
✅ Created index on tax_schemes.item_name
...
✅ Created admin user: Admin
   Password: Admin123
   Role: admin

📊 DATABASE INITIALIZATION SUMMARY
≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

📁 Collection Counts:
   tax_schemes: 6 documents
   pending_updates: 0 documents
   audit_logs: 0 documents
   users: 1 documents

👤 Admin User:
   Username: Admin
   Email: admin@lexauditflow.com
   Role: admin

📋 Sample Tax Schemes:
   - Mobile Phones: 18%
   - Laptops: 18%
   - Tablets: 12%
   - Software: 18%
   - Cloud Services: 18%
   - Data Services: 18%

════════════════════════════════════════════════════════════════
✅ Database initialization complete!
════════════════════════════════════════════════════════════════

✅ Database initialization successful!

📋 Admin Credentials:
   Username: Admin
   Password: Admin123

📍 Database: lexaudit_flow
📍 Collections: tax_schemes, pending_updates, audit_logs, users

Next steps:
1. Start the backend: cd backend && python main.py
2. Start the frontend: cd frontend && npm run dev
3. Open dashboard: http://localhost:5173

╔════════════════════════════════════════════════════════════════╗
║     ✅ Database Setup Complete!                               ║
╚════════════════════════════════════════════════════════════════╝
```

**✅ CONGRATULATIONS! Database is ready!**

---

## 📋 SAVE THESE CREDENTIALS!

```
Username: Admin
Password: Admin123
```

**Keep these safe - you'll need them to login!**

---

## 🔍 Optional: Verify in MongoDB

```powershell
# In the first terminal (mongosh), type:

use lexaudit_flow
show collections
db.tax_schemes.find()
db.users.find()
```

You'll see all the data that was created!

---

## ✅ Checklist - Is Your Database Ready?

- [ ] `.\setup_database.ps1` completed successfully
- [ ] Green ✅ checkmarks appear
- [ ] Message says "Database initialization successful!"
- [ ] You have Admin credentials (Admin / Admin123)
- [ ] `mongosh` is still running in terminal 1
- [ ] You can see collections with `mongosh`

---

## 🚀 What's Next?

### Open Terminal 3 (Backend)

```powershell
cd backend
python main.py

You should see:
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Keep this running**

---

### Open Terminal 4 (Frontend)

```powershell
cd frontend
npm run dev

You should see:
➜  Local:   http://localhost:5173/
```

**✅ Keep this running**

---

### Open Your Browser

```
http://localhost:5173
```

**🎉 You should see the LexAudit Flow Dashboard!**

---

## 📊 Your Terminal Layout Should Look Like This:

```
┌─────────────────────────────────────────────────────────────┐
│ Terminal 1: mongosh                                         │
│ test>  ← MongoDB running                                    │
├─────────────────────────────────────────────────────────────┤
│ Terminal 2: Database setup ✅ COMPLETE                      │
├─────────────────────────────────────────────────────────────┤
│ Terminal 3: Backend (python main.py)                        │
│ INFO: Uvicorn running on http://0.0.0.0:8000 ✅ RUNNING    │
├─────────────────────────────────────────────────────────────┤
│ Terminal 4: Frontend (npm run dev)                          │
│ ➜  Local:   http://localhost:5173/ ✅ RUNNING              │
├─────────────────────────────────────────────────────────────┤
│ Browser: http://localhost:5173                              │
│ Dashboard displays: LexAudit Flow Manager ✅ WORKS          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Success Indicators

### Visual Cues That Everything Works:

✅ **MongoDB Running**
```
Test> prompt appears in mongosh
```

✅ **Database Created**
```
✅ Successfully created database lexaudit_flow
✅ All collections created
✅ Admin user created
```

✅ **Backend Running**
```
INFO:     Started server process
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Frontend Running**
```
VITE v5.0.8 ready
➜  Local:   http://localhost:5173
```

✅ **Dashboard Opens**
```
Browser shows:
- LexAudit Flow header
- Tax Change Alerts section
- Dashboard interface
```

---

## 🚨 If Something Goes Wrong

### Problem: "Connection refused"
```
Solution: Make sure mongosh is running in terminal 1!
```

### Problem: "setup_database.ps1 cannot be loaded"
```powershell
# Run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
.\setup_database.ps1
```

### Problem: "Database already exists"
```
This is NORMAL! The script checks for existing data.
It's safe to run multiple times.
```

### Problem: "Admin user already exists"
```
This is NORMAL! The script skips if admin is already there.
You can proceed with Admin / Admin123 credentials.
```

---

## 📱 Login to Dashboard

Once everything is running:

```
URL: http://localhost:5173

When prompted:
Username: Admin
Password: Admin123
```

---

## 🎊 COMPLETE SUCCESS PATH

```
1. ✅ Run .\setup_database.ps1
   ↓
2. ✅ See success message with Admin / Admin123
   ↓
3. ✅ Start backend: python main.py
   ↓
4. ✅ Start frontend: npm run dev
   ↓
5. ✅ Open http://localhost:5173
   ↓
6. ✅ Login with Admin / Admin123
   ↓
7. 🎉 USE THE DASHBOARD!
```

---

## 💡 Quick Tips

- **Keep MongoDB running**: Don't close the mongosh terminal
- **Multiple runs are safe**: Script won't duplicate data
- **Save admin password**: Admin / Admin123 (use for login)
- **Clear messages**: Script shows exactly what's happening
- **Check status**: Type `db.tax_schemes.find()` in mongosh to see data

---

## 📞 Still Need Help?

Files to read in order:
1. This file (currently reading) ✅
2. `QUICK_DATABASE_SETUP.md` - 5-minute quick guide
3. `DATABASE_SETUP.md` - Detailed reference
4. `DATABASE_SETUP_SUMMARY.md` - Complete summary

---

## 🎯 Your Current Status

```
✅ Database Scripts Created
✅ Config with Admin Credentials Created
✅ Setup Guide Complete
↓
READY FOR: Run setup_database.ps1
↓
You are here! 👈
```

---

## 🚀 Ready? Let's Go!

### Right Now:

```powershell
# Terminal 1: MongoDB
mongosh

# Terminal 2: Database Setup
cd E:\dharmananda\LexAudit_Flow
.\setup_database.ps1

# Watch for ✅ success message
# Note the Admin credentials
```

**Then follow the next steps section to start backend and frontend!**

---

**You've Got This! 🎉**

The database setup takes about 5 minutes total.
Then everything else is straightforward!

**Next: Run the setup script and watch the magic happen!** ✨
