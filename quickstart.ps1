# LexAudit Flow - Quick Start Script for Windows PowerShell
# Run this script to set up and start all services

Write-Host "================================" -ForegroundColor Cyan
Write-Host "LexAudit Flow - Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

$prereqsMet = $true

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.10+" -ForegroundColor Red
    $prereqsMet = $false
} else {
    Write-Host "✅ Python installed" -ForegroundColor Green
}

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    $prereqsMet = $false
} else {
    Write-Host "✅ Node.js installed" -ForegroundColor Green
}

# Check MongoDB
if (-not (Get-Command mongosh -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  MongoDB command-line tool not found. Ensure MongoDB is running." -ForegroundColor Yellow
} else {
    Write-Host "✅ MongoDB CLI available" -ForegroundColor Green
}

# Check Ollama
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Ollama not found. Please install from https://ollama.ai" -ForegroundColor Red
    $prereqsMet = $false
} else {
    Write-Host "✅ Ollama installed" -ForegroundColor Green
}

if (-not $prereqsMet) {
    Write-Host ""
    Write-Host "Please install missing prerequisites and try again." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ All prerequisites met!" -ForegroundColor Green
Write-Host ""

# Ask user what they want to do
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host "1. Install dependencies (first time setup)" -ForegroundColor White
Write-Host "2. Start all services" -ForegroundColor White
Write-Host "3. Install dependencies + Start services" -ForegroundColor White
Write-Host "4. Check service status" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-4)"

if ($choice -eq "1" -or $choice -eq "3") {
    Write-Host ""
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    
    # Backend setup
    Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
    Set-Location backend
    
    if (-not (Test-Path venv)) {
        python -m venv venv
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    }
    
    . .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt --quiet
    playwright install --quiet
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
    
    # Frontend setup
    Set-Location ..\frontend
    npm install --silent
    Write-Host "✅ Node.js dependencies installed" -ForegroundColor Green
    Set-Location ..
}

if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host ""
    Write-Host "🚀 Starting services..." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "IMPORTANT: Ensure the following are running in separate terminals:" -ForegroundColor Yellow
    Write-Host "1. MongoDB: mongosh" -ForegroundColor White
    Write-Host "2. Ollama: ollama serve" -ForegroundColor White
    Write-Host ""
    Write-Host "Starting backend and frontend..." -ForegroundColor Cyan
    Write-Host ""
    
    # Start backend
    $backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; . .\venv\Scripts\Activate.ps1; python main.py" -PassThru
    Write-Host "✅ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
    
    # Wait a moment for backend to start
    Start-Sleep -Seconds 3
    
    # Start frontend
    $frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -PassThru
    Write-Host "✅ Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "🎉 Services Started Successfully!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access the application:" -ForegroundColor Cyan
    Write-Host "📱 Frontend:  http://localhost:5173" -ForegroundColor White
    Write-Host "⚙️  Backend:   http://localhost:8000" -ForegroundColor White
    Write-Host "📊 API Docs:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Services PIDs:" -ForegroundColor Cyan
    Write-Host "Backend: $($backendProcess.Id)" -ForegroundColor White
    Write-Host "Frontend: $($frontendProcess.Id)" -ForegroundColor White
    Write-Host ""
    Write-Host "To stop services, close the terminal windows." -ForegroundColor Yellow
    Write-Host ""
}

if ($choice -eq "4") {
    Write-Host ""
    Write-Host "🔍 Checking service status..." -ForegroundColor Cyan
    Write-Host ""
    
    try {
        $backend = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 2
        if ($backend.StatusCode -eq 200) {
            Write-Host "✅ Backend is running on http://localhost:8000" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Backend is not running" -ForegroundColor Red
    }
    
    try {
        $frontend = Invoke-WebRequest -Uri "http://localhost:5173/" -TimeoutSec 2
        if ($frontend.StatusCode -eq 200) {
            Write-Host "✅ Frontend is running on http://localhost:5173" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Frontend is not running" -ForegroundColor Red
    }
    
    try {
        $ollama = Invoke-WebRequest -Uri "http://localhost:11434/" -TimeoutSec 2
        if ($ollama.StatusCode -eq 200) {
            Write-Host "✅ Ollama is running on http://localhost:11434" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Ollama is not running" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host ""
Write-Host "For detailed setup instructions, see SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
