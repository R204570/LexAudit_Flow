# LexAudit Flow - Database Setup Script
# This script initializes the MongoDB database with required collections and sample data
# Run this AFTER MongoDB is running!

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     LexAudit Flow - Database Setup Script                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB is running
Write-Host "🔍 Checking MongoDB connection..." -ForegroundColor Yellow
try {
    $mongosh = Invoke-Expression "mongosh --eval 'quit()'" 2>&1
    Write-Host "✅ MongoDB is running" -ForegroundColor Green
} catch {
    Write-Host "❌ MongoDB is NOT running!" -ForegroundColor Red
    Write-Host "   Please start MongoDB with: mongosh" -ForegroundColor Yellow
    Write-Host "   Or ensure MongoDB service is running" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📦 Initializing database..." -ForegroundColor Yellow

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host "   Please ensure Python is installed and in PATH" -ForegroundColor Yellow
    exit 1
}

# Navigate to backend directory
$backendPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $backendPath "backend"

if (-not (Test-Path $backendPath)) {
    $backendPath = ".\backend"
}

Write-Host ""
Write-Host "Running initialization script..." -ForegroundColor Cyan
Write-Host ""

# Run the initialization script
try {
    # Try to activate venv if it exists
    $venvPath = Join-Path $backendPath "venv"
    if (Test-Path $venvPath) {
        Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
        & "$venvPath\Scripts\Activate.ps1" 2>$null
    }
    
    # Run the init script
    & python (Join-Path $backendPath "init_database.py")
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Database initialization successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Admin Credentials:" -ForegroundColor Cyan
        Write-Host "   Username: Admin" -ForegroundColor White
        Write-Host "   Password: Admin123" -ForegroundColor White
        Write-Host ""
        Write-Host "📍 Database: lexaudit_flow" -ForegroundColor Cyan
        Write-Host "📍 Collections: tax_schemes, pending_updates, audit_logs, users" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Start the backend: cd backend && python main.py" -ForegroundColor White
        Write-Host "2. Start the frontend: cd frontend && npm run dev" -ForegroundColor White
        Write-Host "3. Open dashboard: http://localhost:5173" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Database initialization failed!" -ForegroundColor Red
        Write-Host "   Check the error messages above" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Error running initialization script:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     ✅ Database Setup Complete!                               ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
