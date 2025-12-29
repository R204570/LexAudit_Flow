from pymongo import MongoClient
from datetime import datetime
from typing import Optional

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lexaudit_flow"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
tax_schemes = db["tax_schemes"]
pending_updates = db["pending_updates"]
audit_logs = db["audit_logs"]

# Create indexes
def init_db():
    """Initialize database indexes"""
    tax_schemes.create_index("item_name", unique=True)
    pending_updates.create_index("status")
    audit_logs.create_index("timestamp")
    print("Database initialized successfully")

# Sample data initialization
def seed_database():
    """Seed database with sample tax schemes"""
    if tax_schemes.count_documents({}) == 0:
        sample_data = [
            {"item_name": "Mobile Phones", "tax_percentage": 18.0, "last_updated": datetime.now()},
            {"item_name": "Laptops", "tax_percentage": 18.0, "last_updated": datetime.now()},
            {"item_name": "Tablets", "tax_percentage": 12.0, "last_updated": datetime.now()},
            {"item_name": "Software", "tax_percentage": 18.0, "last_updated": datetime.now()},
        ]
        tax_schemes.insert_many(sample_data)
        print("Sample data seeded")
