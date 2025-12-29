#!/bin/bash
# LexAudit Flow - Database Setup Script (for Linux/macOS)
# This script initializes the MongoDB database

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     LexAudit Flow - Database Setup Script                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if MongoDB is running
echo "🔍 Checking MongoDB connection..."
if ! command -v mongosh &> /dev/null; then
    echo "❌ MongoDB is NOT running!"
    echo "   Please start MongoDB with: mongosh"
    exit 1
fi

# Test MongoDB connection
mongosh --eval "quit()" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ MongoDB is NOT running!"
    echo "   Please start MongoDB with: mongosh"
    exit 1
fi

echo "✅ MongoDB is running"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python not found!"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "📦 Initializing database..."
echo ""

# Navigate to backend directory and run init script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_PATH="$SCRIPT_DIR/backend"

# Check if venv exists and activate it
if [ -d "$BACKEND_PATH/venv" ]; then
    echo "🔄 Activating virtual environment..."
    source "$BACKEND_PATH/venv/bin/activate"
fi

# Run the initialization script
echo "Running initialization script..."
echo ""

$PYTHON_CMD "$BACKEND_PATH/init_database.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database initialization successful!"
    echo ""
    echo "📋 Admin Credentials:"
    echo "   Username: Admin"
    echo "   Password: Admin123"
    echo ""
    echo "📍 Database: lexaudit_flow"
    echo "📍 Collections: tax_schemes, pending_updates, audit_logs, users"
    echo ""
    echo "Next steps:"
    echo "1. Start the backend: cd backend && python main.py"
    echo "2. Start the frontend: cd frontend && npm run dev"
    echo "3. Open dashboard: http://localhost:5173"
    echo ""
else
    echo ""
    echo "❌ Database initialization failed!"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     ✅ Database Setup Complete!                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
