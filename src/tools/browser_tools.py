"""Browser interaction tools for LangManus Demo."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
import logging
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)


def fetch_webpage(url: str, timeout: int = 30) -> Dict[str, Any]:
    """Fetch content from a webpage.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Dict containing page content and metadata
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract basic metadata
        title = soup.find('title')
        title_text = title.text.strip() if title else "No title"
        
        # Extract text content
        for script in soup(["script", "style"]):
            script.decompose()
        
        text_content = soup.get_text()
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return {
            "success": True,
            "url": url,
            "title": title_text,
            "content": clean_text[:10000],  # Limit content length
            "html": response.text[:20000],  # Limit HTML length
            "status_code": response.status_code,
            "encoding": response.encoding
        }
        
    except requests.RequestException as e:
        logger.error(f"Error fetching webpage {url}: {e}")
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "content": "",
            "html": ""
        }
    except Exception as e:
        logger.error(f"Error processing webpage {url}: {e}")
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "content": "",
            "html": ""
        }


def get_page_metadata(url: str) -> Dict[str, Any]:
    """Extract metadata from a webpage.
    
    Args:
        url: URL to extract metadata from
        
    Returns:
        Dict containing page metadata
    """
    try:
        page_data = fetch_webpage(url)
        
        if not page_data["success"]:
            return {
                "success": False,
                "error": page_data["error"],
                "metadata": {}
            }
        
        soup = BeautifulSoup(page_data["html"], 'html.parser')
        
        metadata = {
            "title": page_data["title"],
            "url": url,
            "content_length": len(page_data["content"])
        }
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        return {
            "success": True,
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"Error extracting metadata from {url}: {e}")
        return {
            "success": False,
            "error": str(e),
            "metadata": {}
        }
