import logging
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

EVIDENCE_DIR = Path(__file__).parent.parent / "evidence"


def generate_proof(pdf_path: str, quote_text: str, update_id: str) -> Optional[str]:
    """
    Generate a highlighted PDF with evidence text marked.
    
    Args:
        pdf_path: Path to the original PDF
        quote_text: Text to highlight in the PDF
        update_id: ID of the update for naming the output file
        
    Returns:
        Path to the highlighted PDF
    """
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Search for the quote text and highlight it
        highlight_count = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Search for text
            text_dict = page.get_text("dict")
            
            # Simple search: find all occurrences of the quote text
            for instance in page.search_for(quote_text):
                # Highlight the found text in yellow
                highlight = page.add_highlight_annot(instance)
                highlight.set_colors({"stroke": [1, 1, 0]})  # Yellow highlight
                highlight_count += 1
        
        if highlight_count == 0:
            logger.warning(f"Quote text '{quote_text}' not found in {pdf_path}")
            # Still save the PDF even if text not found
        
        # Save the highlighted PDF
        output_path = EVIDENCE_DIR / "highlighted" / f"{update_id}_highlighted.pdf"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        logger.info(f"Highlighted PDF saved: {output_path} ({highlight_count} highlights)")
        return str(output_path)
        
    except Exception as e:
        logger.error(f"Error generating proof for {pdf_path}: {e}")
        return None
