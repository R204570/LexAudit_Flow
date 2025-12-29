# 🚀 Database Setup - Quick Start Guide

## ⚡ Super Quick (5 minutes)

### Step 1: Start MongoDB
```powershell
mongosh
# Keep this terminal open
```

### Step 2: Setup Database (in NEW terminal)
```powershell
# From project root
.\setup_database.ps1
```

### Step 3: Done!
You'll see:
```
✅ Database initialization successful!

📋 Admin Credentials:
   Username: Admin
   Password: Admin123
```

---

## 📋 What Gets Created

| Item | Details |
|------|---------|
| **Database** | `lexaudit_flow` |
| **Collections** | tax_schemes, pending_updates, audit_logs, users |
| **Admin User** | Username: `Admin`, Password: `Admin123` |
| **Sample Data** | 6 tax items (Mobile Phones, Laptops, etc.) |
| **Indexes** | Automatic indexes for performance |

---

## 🔍 Verify It Worked

```powershell
mongosh

# Check collections
use lexaudit_flow
show collections

# See admin user
db.users.find()

# See tax data
db.tax_schemes.find()
```

You should see the sample data!

---

## ✅ Success Checklist

- [ ] MongoDB is running (`mongosh` connects)
- [ ] `.\setup_database.ps1` runs without errors
- [ ] You see "✅ Database initialization successful!"
- [ ] Admin credentials displayed
- [ ] `mongosh` can access `lexaudit_flow` database

---

## 📝 Admin Credentials (Save These!)

```
Username: Admin
Password: Admin123
Database: lexaudit_flow
```

Use these to login to the dashboard later.

---

## 🚨 Troubleshooting

**Q: "Connection refused"**
A: Make sure MongoDB is running with `mongosh`

**Q: "Database already exists"**
A: Normal! Script checks for existing data and won't duplicate

**Q: "Admin user already exists"**
A: Normal! Script skips if running again

**Q: Setup script not found**
A: Make sure you're in project root (where README.md is)

---

## 🎯 Next Steps After Database Setup

1. ✅ Database created ← **YOU ARE HERE**
2. Start backend: `cd backend && python main.py`
3. Start frontend: `cd frontend && npm run dev`
4. Open dashboard: `http://localhost:5173`

---

## 🔗 Files Created

| File | Purpose |
|------|---------|
| `init_database.py` | Python script that creates everything |
| `setup_database.ps1` | Windows PowerShell launcher |
| `setup_database.sh` | Linux/macOS launcher |
| `config.py` | Configuration (Admin credentials) |
| `DATABASE_SETUP.md` | Detailed guide (this file) |

---

## 💡 Tips

- Keep MongoDB terminal open while using the app
- The setup script is safe to run multiple times
- If you need to reset: delete database with `db.dropDatabase()` then re-run script
- Admin password is stored plain in dev mode (hash for production!)

---

**Setup Time**: ~5 minutes
**Difficulty**: ⭐ (Very Easy)
**Next**: Start backend & frontend, then open dashboard!

Happy auditing! 🎉
