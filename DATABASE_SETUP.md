# LexAudit Flow - Database Setup Guide

## 🚀 Quick Database Setup

### Option 1: Windows PowerShell (Recommended)

```powershell
# 1. Start MongoDB in a terminal
mongosh

# 2. Run database setup (in a NEW terminal, from project root)
.\setup_database.ps1

# Expected output:
# ✅ Database initialization successful!
# Admin Credentials:
#    Username: Admin
#    Password: Admin123
```

### Option 2: Linux/macOS

```bash
# 1. Start MongoDB
mongosh

# 2. Run database setup (in a new terminal, from project root)
chmod +x setup_database.sh
./setup_database.sh

# Expected output:
# ✅ Database initialization successful!
```

### Option 3: Manual Python

```powershell
# Make sure you're in the project root
cd backend

# Activate virtual environment (if exists)
.\venv\Scripts\Activate.ps1

# Run the initialization script
python init_database.py
```

---

## 📋 What Gets Created

### Collections

**1. tax_schemes** (Source of Truth)
```javascript
{
  _id: ObjectId,
  item_name: String,          // "Mobile Phones"
  tax_percentage: Float,      // 18.0
  last_updated: DateTime,
  description: String
}
```

**2. pending_updates** (AI Recommendations)
```javascript
{
  _id: ObjectId,
  detected_item: String,
  current_db_val: Float,
  new_web_val: Float,
  evidence_pdf_path: String,
  evidence_quote: String,
  status: String,             // "pending", "accepted", "rejected"
  created_at: DateTime,
  updated_at: DateTime
}
```

**3. audit_logs** (Decision History)
```javascript
{
  _id: ObjectId,
  action: String,             // "update_accepted", "update_rejected"
  item_name: String,
  old_value: Float,
  new_value: Float,
  timestamp: DateTime
}
```

**4. users** (Authentication)
```javascript
{
  _id: ObjectId,
  username: String,           // "Admin"
  password: String,           // "Admin123" (⚠️ plain in dev, hash in prod)
  email: String,
  role: String,               // "admin"
  created_at: DateTime,
  is_active: Boolean
}
```

---

## 👤 Admin User

After setup, you'll have:

```
Username: Admin
Password: Admin123
Email: admin@lexauditflow.com
Role: admin
```

---

## 📊 Sample Data

The script auto-seeds `tax_schemes` with:

| Item | Rate |
|------|------|
| Mobile Phones | 18% |
| Laptops | 18% |
| Tablets | 12% |
| Software | 18% |
| Cloud Services | 18% |
| Data Services | 18% |

---

## 🔍 Verify Database

After setup, verify with MongoDB client:

```powershell
# Open MongoDB shell
mongosh

# Switch to database
use lexaudit_flow

# Check collections
show collections

# View sample data
db.tax_schemes.find()
db.users.find()

# Count documents
db.tax_schemes.countDocuments()
db.users.countDocuments()
```

---

## 🐛 Troubleshooting

### Error: "Connection refused"
```
Solution: Ensure MongoDB is running
- Run: mongosh
- Or start MongoDB service
```

### Error: "Database already exists"
```
This is normal! The script checks for existing data.
It won't duplicate if run multiple times.
```

### Error: "Admin user already exists"
```
This is normal! If running setup again, it skips existing admin.
To reset admin password, see below.
```

---

## 🔄 Reset Database

To completely reset (⚠️ deletes all data):

```powershell
mongosh

# Switch to database
use lexaudit_flow

# Drop all collections
db.tax_schemes.deleteMany({})
db.pending_updates.deleteMany({})
db.audit_logs.deleteMany({})
db.users.deleteMany({})

# Or drop entire database
db.dropDatabase()

# Exit
quit()
```

Then re-run: `.\setup_database.ps1`

---

## 🔐 Security Notes

⚠️ **Important for Production:**

1. **Password Hashing**: The current setup stores plain text passwords. For production:
   ```python
   import bcrypt
   
   # Hash password
   hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   
   # Verify password
   bcrypt.checkpw(password.encode(), hashed)
   ```

2. **Authentication**: Implement JWT tokens or session management

3. **Encryption**: Use MongoDB encryption at rest

4. **Access Control**: Use MongoDB RBAC (Role-Based Access Control)

---

## 📝 Configuration

Database connection settings in `backend/config.py`:

```python
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lexaudit_flow"

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "Admin123"
```

To change MongoDB URI (e.g., for Atlas):

```python
MONGO_URI = "mongodb+srv://user:password@cluster.mongodb.net/lexaudit_flow"
```

---

## 📚 Script Files

### `init_database.py`
Python script that:
- Connects to MongoDB
- Creates collections
- Creates indexes
- Seeds sample data
- Creates admin user

### `setup_database.ps1`
PowerShell wrapper that:
- Checks MongoDB connection
- Activates venv
- Runs `init_database.py`
- Displays results

### `setup_database.sh`
Bash wrapper for Linux/macOS

---

## ✅ After Database Setup

1. ✅ Database created
2. ✅ Collections ready
3. ✅ Indexes created
4. ✅ Sample data seeded
5. ✅ Admin user created

**Next Steps:**
- Start backend: `cd backend && python main.py`
- Start frontend: `cd frontend && npm run dev`
- Open dashboard: `http://localhost:5173`

---

## 🔗 Database Connection in Code

The backend connects automatically:

```python
# In backend/core/db.py
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections automatically available
db.tax_schemes
db.pending_updates
db.audit_logs
db.users
```

---

## 📊 Monitoring Database

View real-time data:

```powershell
# Watch for new updates
mongosh
use lexaudit_flow
db.pending_updates.watch()

# Monitor audit logs
db.audit_logs.find().sort({timestamp: -1}).limit(10)

# Check user activity
db.users.find()
```

---

## 🎯 Success Indicators

Database setup is complete when:

- ✅ Setup script runs without errors
- ✅ `mongosh` shows `lexaudit_flow` database
- ✅ All 4 collections exist
- ✅ Admin user can be found: `db.users.findOne({username: "Admin"})`
- ✅ Tax schemes have sample data
- ✅ Backend can connect successfully

---

## 📞 Common Questions

**Q: Can I use MongoDB Atlas instead of local?**
A: Yes, change MONGO_URI in `config.py` to your Atlas connection string

**Q: How do I add more tax items?**
A: Insert into tax_schemes collection:
```javascript
db.tax_schemes.insertOne({
  item_name: "New Item",
  tax_percentage: 18.0,
  last_updated: new Date()
})
```

**Q: How do I change admin password?**
A: Update in MongoDB:
```javascript
db.users.updateOne(
  {username: "Admin"},
  {$set: {password: "NewPassword123"}}
)
```

**Q: Can I have multiple admin users?**
A: Yes, modify `init_database.py` to create more users with `role: "admin"`

---

**Database Setup Version**: 1.0
**Last Updated**: January 1, 2024
