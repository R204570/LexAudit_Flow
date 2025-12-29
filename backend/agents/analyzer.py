import json
import logging
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF
import ollama
from core.models import AnalysisResult
from core.db import tax_schemes, pending_updates
from datetime import datetime

logger = logging.getLogger(__name__)

EVIDENCE_DIR = Path(__file__).parent.parent / "evidence"
OLLAMA_MODEL = "llama2"  # or "llama2:13b" for more accuracy
OLLAMA_BASE_URL = "http://localhost:11434"


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {e}")
        return ""


def analyze_document(pdf_path: str) -> Optional[AnalysisResult]:
    """
    Analyze a PDF document using Ollama/Llama model.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        AnalysisResult with change detection info
    """
    try:
        # Extract text from PDF
        pdf_text = extract_pdf_text(pdf_path)
        if not pdf_text:
            logger.warning(f"No text extracted from {pdf_path}")
            return None
        
        # Get current database values
        db_items = list(tax_schemes.find())
        db_context = "\n".join([
            f"- {item['item_name']}: {item['tax_percentage']}%"
            for item in db_items
        ])
        
        # Prepare prompt for Ollama
        system_prompt = """You are a Tax Auditor. I will provide current database values and a new document text. 
If the tax percentage for an item has changed, return ONLY valid JSON: 
{ "change_detected": true, "item": "item_name", "new_val": 12.0, "quote": "exact text from doc" }
If no change, return ONLY:
{ "change_detected": false }
Do not include any other text. Return ONLY the JSON."""
        
        user_prompt = f"""Current Database Values:
{db_context}

New Document Text:
{pdf_text}

Analyze and detect any tax percentage changes."""
        
        # Call Ollama/Llama
        logger.info(f"Analyzing document: {pdf_path}")
        response = ollama.generate(
            model=OLLAMA_MODEL,
            prompt=user_prompt,
            system=system_prompt,
            stream=False,
        )
        
        # Parse response
        response_text = response.get("response", "").strip()
        logger.info(f"Ollama Response: {response_text}")
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result_data = json.loads(json_str)
            else:
                result_data = json.loads(response_text)
            
            result = AnalysisResult(**result_data)
            
            # If change detected, store in pending_updates
            if result.change_detected:
                logger.info(f"Change detected: {result.item} -> {result.new_val}")
                store_pending_update(
                    detected_item=result.item,
                    new_web_val=result.new_val,
                    evidence_pdf_path=pdf_path,
                    evidence_quote=result.quote
                )
            
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response_text}, Error: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error analyzing document {pdf_path}: {e}")
        return None


def store_pending_update(
    detected_item: str,
    new_web_val: float,
    evidence_pdf_path: str,
    evidence_quote: str
) -> str:
    """Store a pending update in the database."""
    try:
        # Find current value in database
        current_item = tax_schemes.find_one({"item_name": detected_item})
        current_db_val = current_item["tax_percentage"] if current_item else None
        
        # Create pending update record
        update_record = {
            "detected_item": detected_item,
            "current_db_val": current_db_val,
            "new_web_val": new_web_val,
            "evidence_pdf_path": evidence_pdf_path,
            "evidence_quote": evidence_quote,
            "status": "pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        
        result = pending_updates.insert_one(update_record)
        logger.info(f"Pending update stored with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error storing pending update: {e}")
        return None
