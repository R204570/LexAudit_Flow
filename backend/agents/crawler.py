import asyncio
import random
from pathlib import Path
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

EVIDENCE_DIR = Path(__file__).parent.parent / "evidence" / "raw"


async def crawl_and_download(url: str) -> list[str]:
    """
    Crawl a website and download PDF documents related to tax/amendments.
    
    Args:
        url: Target URL to crawl
        
    Returns:
        List of paths to downloaded PDFs
    """
    downloaded_files = []
    ua = UserAgent()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=ua.random,
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        try:
            logger.info(f"Crawling URL: {url}")
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Random delay to mimic human behavior
            await asyncio.sleep(random.uniform(2, 5))
            
            # Find all links
            links = await page.locator("a").all()
            
            for link in links:
                href = await link.get_attribute("href")
                text = await link.text_content()
                
                if href and text:
                    # Check if link contains tax-related keywords
                    keywords = ["tax", "amendment", "scheme", "regulation", "pdf"]
                    if any(kw.lower() in (text.lower() + href.lower()) for kw in keywords):
                        # Resolve relative URLs
                        if href.startswith("http"):
                            pdf_url = href
                        else:
                            pdf_url = url.rstrip("/") + "/" + href.lstrip("/")
                        
                        if pdf_url.lower().endswith(".pdf"):
                            try:
                                logger.info(f"Downloading PDF: {pdf_url}")
                                file_name = pdf_url.split("/")[-1] or f"document_{len(downloaded_files)}.pdf"
                                file_path = EVIDENCE_DIR / file_name
                                
                                # Download PDF using Playwright's download feature
                                async with await context.expect_download() as download_info:
                                    await link.click()
                                download = await download_info.value
                                await download.save_as(file_path)
                                
                                downloaded_files.append(str(file_path))
                                logger.info(f"Downloaded: {file_path}")
                                
                                # Random delay between downloads
                                await asyncio.sleep(random.uniform(1, 3))
                            except Exception as e:
                                logger.warning(f"Failed to download {pdf_url}: {e}")
            
        except Exception as e:
            logger.error(f"Crawling error for {url}: {e}")
        finally:
            await context.close()
            await browser.close()
    
    return downloaded_files


def sync_crawl_and_download(url: str) -> list[str]:
    """Synchronous wrapper for crawl_and_download"""
    return asyncio.run(crawl_and_download(url))
