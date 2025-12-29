"""
LexAudit Flow - Configuration File
Contains all configuration settings for the application
"""

# Database Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lexaudit_flow"

# Admin Credentials
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "Admin123"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_DEBUG = True

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"

# Application Settings
CRAWL_TIMEOUT = 60000  # milliseconds
PDF_SEARCH_KEYWORDS = ["tax", "amendment", "scheme", "regulation", "policy"]
MAX_PDF_DOWNLOADS = 20

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "*"  # Allow all in development (remove for production)
]

# Feature Flags
ENABLE_CRAWLING = True
ENABLE_AI_ANALYSIS = True
ENABLE_PDF_HIGHLIGHTING = True
ENABLE_AUDIT_LOGGING = True
