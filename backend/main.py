import logging
import os
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, HTTPException, StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from core.db import init_db, seed_database, tax_schemes, pending_updates, audit_logs
from core.models import PendingUpdate, UpdateResponse, UpdateAcceptRequest, TaxScheme
from agents.crawler import sync_crawl_and_download
from agents.analyzer import analyze_document
from agents.highlighter import generate_proof

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="LexAudit Flow", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    seed_database()
    logger.info("Application started successfully")

# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "LexAudit Flow Backend is running"}


@app.get("/tax-schemes")
async def get_tax_schemes():
    """Fetch all tax schemes from the database"""
    try:
        schemes = list(tax_schemes.find())
        # Convert ObjectId to string for JSON serialization
        for scheme in schemes:
            scheme["_id"] = str(scheme["_id"])
        return schemes
    except Exception as e:
        logger.error(f"Error fetching tax schemes: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tax schemes")


@app.get("/updates")
async def get_pending_updates():
    """Fetch all pending updates"""
    try:
        updates = list(pending_updates.find({"status": "pending"}))
        result = []
        for update in updates:
            result.append({
                "id": str(update["_id"]),
                "detected_item": update["detected_item"],
                "current_db_val": update["current_db_val"],
                "new_web_val": update["new_web_val"],
                "evidence_pdf_path": update["evidence_pdf_path"],
                "evidence_quote": update["evidence_quote"],
                "status": update["status"],
                "created_at": update["created_at"].isoformat() if isinstance(update["created_at"], datetime) else update["created_at"],
            })
        return result
    except Exception as e:
        logger.error(f"Error fetching pending updates: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pending updates")


@app.get("/updates/{update_id}")
async def get_update_detail(update_id: str):
    """Get details of a specific update"""
    try:
        update = pending_updates.find_one({"_id": ObjectId(update_id)})
        if not update:
            raise HTTPException(status_code=404, detail="Update not found")
        
        return {
            "id": str(update["_id"]),
            "detected_item": update["detected_item"],
            "current_db_val": update["current_db_val"],
            "new_web_val": update["new_web_val"],
            "evidence_pdf_path": update["evidence_pdf_path"],
            "evidence_quote": update["evidence_quote"],
            "status": update["status"],
            "created_at": update["created_at"].isoformat() if isinstance(update["created_at"], datetime) else update["created_at"],
        }
    except Exception as e:
        logger.error(f"Error fetching update {update_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch update")


@app.post("/updates/{update_id}/accept")
async def accept_update(update_id: str, request: UpdateAcceptRequest):
    """Accept or reject a pending update"""
    try:
        update = pending_updates.find_one({"_id": ObjectId(update_id)})
        if not update:
            raise HTTPException(status_code=404, detail="Update not found")
        
        if request.accept:
            # Update the tax_schemes collection
            item_name = update["detected_item"]
            new_value = update["new_web_val"]
            
            # Get old value before update
            old_item = tax_schemes.find_one({"item_name": item_name})
            old_value = old_item["tax_percentage"] if old_item else None
            
            # Update tax scheme
            result = tax_schemes.update_one(
                {"item_name": item_name},
                {
                    "$set": {
                        "tax_percentage": new_value,
                        "last_updated": datetime.now()
                    }
                },
                upsert=True
            )
            
            # Mark update as accepted
            pending_updates.update_one(
                {"_id": ObjectId(update_id)},
                {
                    "$set": {
                        "status": "accepted",
                        "updated_at": datetime.now()
                    }
                }
            )
            
            # Log to audit_logs
            audit_logs.insert_one({
                "action": "update_accepted",
                "item_name": item_name,
                "old_value": old_value,
                "new_value": new_value,
                "timestamp": datetime.now(),
            })
            
            logger.info(f"Update {update_id} accepted: {item_name} -> {new_value}")
            return {"status": "accepted", "message": "Update accepted successfully"}
        else:
            # Reject the update
            pending_updates.update_one(
                {"_id": ObjectId(update_id)},
                {
                    "$set": {
                        "status": "rejected",
                        "updated_at": datetime.now()
                    }
                }
            )
            
            audit_logs.insert_one({
                "action": "update_rejected",
                "item_name": update["detected_item"],
                "old_value": update["current_db_val"],
                "new_value": update["new_web_val"],
                "timestamp": datetime.now(),
            })
            
            logger.info(f"Update {update_id} rejected")
            return {"status": "rejected", "message": "Update rejected"}
            
    except Exception as e:
        logger.error(f"Error processing update {update_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process update")


@app.get("/evidence/{filename}")
async def get_evidence_file(filename: str):
    """Serve the highlighted PDF files"""
    try:
        file_path = Path(__file__).parent / "evidence" / "highlighted" / filename
        
        if not file_path.exists():
            # Try raw evidence folder
            file_path = Path(__file__).parent / "evidence" / "raw" / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Evidence file not found")
        
        return FileResponse(file_path, media_type="application/pdf", filename=filename)
    except Exception as e:
        logger.error(f"Error serving evidence file {filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to serve evidence file")


@app.post("/crawl")
async def trigger_crawl(url: str):
    """Trigger a manual crawl of a website"""
    try:
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        logger.info(f"Starting crawl for URL: {url}")
        downloaded_files = sync_crawl_and_download(url)
        
        # Analyze each downloaded PDF
        analysis_results = []
        for pdf_path in downloaded_files:
            result = analyze_document(pdf_path)
            if result:
                analysis_results.append({
                    "pdf": pdf_path,
                    "change_detected": result.change_detected,
                    "item": result.item,
                    "new_val": result.new_val,
                })
                
                # Generate highlighted PDF if change detected
                if result.change_detected:
                    # Find the pending update we just created
                    pending = pending_updates.find_one(
                        {"detected_item": result.item, "status": "pending"},
                        sort=[("created_at", -1)]
                    )
                    if pending:
                        highlighted_path = generate_proof(
                            pdf_path,
                            result.quote,
                            str(pending["_id"])
                        )
                        # Update the pending update with highlighted path
                        if highlighted_path:
                            pending_updates.update_one(
                                {"_id": pending["_id"]},
                                {"$set": {"evidence_pdf_path": highlighted_path}}
                            )
        
        return {
            "status": "completed",
            "downloaded_files": downloaded_files,
            "analysis_results": analysis_results,
        }
    except Exception as e:
        logger.error(f"Error during crawl: {e}")
        raise HTTPException(status_code=500, detail="Crawl failed")


@app.get("/audit-logs")
async def get_audit_logs():
    """Fetch all audit logs"""
    try:
        logs = list(audit_logs.find().sort("timestamp", -1))
        result = []
        for log in logs:
            result.append({
                "id": str(log["_id"]),
                "action": log["action"],
                "item_name": log["item_name"],
                "old_value": log["old_value"],
                "new_value": log["new_value"],
                "timestamp": log["timestamp"].isoformat() if isinstance(log["timestamp"], datetime) else log["timestamp"],
            })
        return result
    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch audit logs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
