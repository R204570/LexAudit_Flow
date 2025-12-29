"""
LexAudit Flow - Database Initialization Script
This script creates and seeds the MongoDB database with collections and sample data.
Admin Credentials: Username=Admin, Password=Admin123
"""

import pymongo
from pymongo import MongoClient
from datetime import datetime
import sys
import getpass
from bson import ObjectId

# Database configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lexaudit_flow"

# Admin credentials (can be overridden)
DEFAULT_ADMIN_USERNAME = "Admin"
DEFAULT_ADMIN_PASSWORD = "Admin123"


def connect_database():
    """Connect to MongoDB"""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB")
        return client
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print(f"   Make sure MongoDB is running on {MONGO_URI}")
        sys.exit(1)


def create_database(client):
    """Create or get database"""
    db = client[DB_NAME]
    print(f"✅ Database '{DB_NAME}' ready")
    return db


def create_collections(db):
    """Create collections"""
    collections_to_create = [
        "tax_schemes",
        "pending_updates",
        "audit_logs",
        "users",  # For future authentication
    ]
    
    existing_collections = db.list_collection_names()
    
    for collection_name in collections_to_create:
        if collection_name not in existing_collections:
            db.create_collection(collection_name)
            print(f"✅ Created collection: {collection_name}")
        else:
            print(f"ℹ️  Collection already exists: {collection_name}")


def create_indexes(db):
    """Create indexes for better performance"""
    try:
        # tax_schemes indexes
        db.tax_schemes.create_index("item_name", unique=True)
        print("✅ Created index on tax_schemes.item_name")
        
        # pending_updates indexes
        db.pending_updates.create_index("status")
        print("✅ Created index on pending_updates.status")
        
        # audit_logs indexes
        db.audit_logs.create_index("timestamp", direction=-1)
        print("✅ Created index on audit_logs.timestamp")
        
        # users indexes
        db.users.create_index("username", unique=True)
        print("✅ Created index on users.username")
        
    except Exception as e:
        print(f"⚠️  Index creation warning: {e}")


def seed_tax_schemes(db):
    """Seed tax_schemes collection with sample data"""
    # Check if data already exists
    existing_count = db.tax_schemes.count_documents({})
    
    if existing_count > 0:
        print(f"ℹ️  tax_schemes already has {existing_count} records, skipping seed")
        return
    
    sample_tax_schemes = [
        {
            "item_name": "Mobile Phones",
            "tax_percentage": 18.0,
            "last_updated": datetime.now(),
            "description": "GST on mobile phones and accessories"
        },
        {
            "item_name": "Laptops",
            "tax_percentage": 18.0,
            "last_updated": datetime.now(),
            "description": "GST on computers and laptops"
        },
        {
            "item_name": "Tablets",
            "tax_percentage": 12.0,
            "last_updated": datetime.now(),
            "description": "GST on tablets and digital devices"
        },
        {
            "item_name": "Software",
            "tax_percentage": 18.0,
            "last_updated": datetime.now(),
            "description": "GST on software licenses"
        },
        {
            "item_name": "Cloud Services",
            "tax_percentage": 18.0,
            "last_updated": datetime.now(),
            "description": "GST on cloud computing services"
        },
        {
            "item_name": "Data Services",
            "tax_percentage": 18.0,
            "last_updated": datetime.now(),
            "description": "GST on data analytics services"
        }
    ]
    
    try:
        result = db.tax_schemes.insert_many(sample_tax_schemes)
        print(f"✅ Inserted {len(result.inserted_ids)} tax schemes")
        
        # Display inserted data
        print("\n📋 Tax Schemes Inserted:")
        for scheme in sample_tax_schemes:
            print(f"   - {scheme['item_name']}: {scheme['tax_percentage']}%")
    except Exception as e:
        print(f"❌ Error inserting tax schemes: {e}")


def create_admin_user(db, username=DEFAULT_ADMIN_USERNAME, password=DEFAULT_ADMIN_PASSWORD):
    """Create admin user"""
    # Check if admin already exists
    existing_admin = db.users.find_one({"username": username})
    
    if existing_admin:
        print(f"ℹ️  Admin user '{username}' already exists")
        return
    
    # In production, you should hash the password
    # For now, storing plain (only for demo/development)
    admin_user = {
        "username": username,
        "password": password,  # ⚠️ In production, HASH this!
        "email": "admin@lexauditflow.com",
        "role": "admin",
        "created_at": datetime.now(),
        "is_active": True,
    }
    
    try:
        result = db.users.insert_one(admin_user)
        print(f"✅ Created admin user: {username}")
        print(f"   Password: {password}")
        print(f"   Role: admin")
        return result.inserted_id
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")


def display_summary(db):
    """Display database summary"""
    print("\n" + "="*60)
    print("📊 DATABASE INITIALIZATION SUMMARY")
    print("="*60)
    
    collections = {
        "tax_schemes": db.tax_schemes.count_documents({}),
        "pending_updates": db.pending_updates.count_documents({}),
        "audit_logs": db.audit_logs.count_documents({}),
        "users": db.users.count_documents({}),
    }
    
    print("\n📁 Collection Counts:")
    for collection, count in collections.items():
        print(f"   {collection}: {count} documents")
    
    print("\n👤 Admin User:")
    admin = db.users.find_one({"role": "admin"})
    if admin:
        print(f"   Username: {admin['username']}")
        print(f"   Email: {admin.get('email', 'N/A')}")
        print(f"   Role: {admin['role']}")
    else:
        print("   No admin user found")
    
    print("\n📋 Sample Tax Schemes:")
    schemes = db.tax_schemes.find().limit(5)
    for scheme in schemes:
        print(f"   - {scheme['item_name']}: {scheme['tax_percentage']}%")
    
    print("\n" + "="*60)
    print("✅ Database initialization complete!")
    print("="*60 + "\n")


def main():
    """Main initialization function"""
    print("\n🚀 LexAudit Flow - Database Initialization")
    print("="*60)
    
    # Step 1: Connect to MongoDB
    print("\n[1/5] Connecting to MongoDB...")
    client = connect_database()
    
    # Step 2: Create or get database
    print("[2/5] Creating/getting database...")
    db = create_database(client)
    
    # Step 3: Create collections
    print("[3/5] Creating collections...")
    create_collections(db)
    
    # Step 4: Create indexes
    print("[4/5] Creating indexes...")
    create_indexes(db)
    
    # Step 5: Seed data and create admin
    print("[5/5] Seeding data and creating admin user...")
    seed_tax_schemes(db)
    create_admin_user(db)
    
    # Display summary
    display_summary(db)
    
    # Close connection
    client.close()
    print("✅ Database connection closed\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Initialization interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
