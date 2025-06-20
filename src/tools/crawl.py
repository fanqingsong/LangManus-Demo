"""Web crawling tools for LangManus Demo."""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from typing import Dict, Any, List, Set, Optional
import time
import logging
from collections import deque
import re

logger = logging.getLogger(__name__)


class WebCrawler:
    """Web crawler for extracting content from websites."""
    
    def __init__(self, delay: float = 1.0, max_depth: int = 2, max_pages: int = 10):
        """Initialize web crawler.
        
        Args:
            delay: Delay between requests in seconds
            max_depth: Maximum crawling depth
            max_pages: Maximum number of pages to crawl
        """
        self.delay = delay
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def crawl_page(self, url: str) -> Dict[str, Any]:
        """Crawl a single page.
        
        Args:
            url: URL to crawl
            
        Returns:
            Dict containing page data
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.text.strip() if title else "No title"
            
            # Extract text content
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            text_content = soup.get_text()
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href'].strip()
                if href and not href.startswith('#'):
                    links.append(href)
            
            return {
                "success": True,
                "url": url,
                "title": title_text,
                "content": clean_text[:5000],  # Limit content length
                "links": links[:50],  # Limit links
                "content_length": len(clean_text),
                "status_code": response.status_code
            }
            
        except Exception as e:
            logger.error(f"Error crawling page {url}: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }


# Global crawler instance
_crawler = WebCrawler()


def crawl_single_page(url: str) -> Dict[str, Any]:
    """Crawl a single page.
    
    Args:
        url: URL to crawl
        
    Returns:
        Dict containing page data
    """
    return _crawler.crawl_page(url)


def extract_links_from_page(url: str) -> Dict[str, Any]:
    """Extract all links from a page.
    
    Args:
        url: URL to extract links from
        
    Returns:
        Dict containing extracted links
    """
    try:
        page_data = _crawler.crawl_page(url)
        if page_data["success"]:
            return {
                "success": True,
                "url": url,
                "links": page_data["links"],
                "total_links": len(page_data["links"])
            }
        else:
            return {
                "success": False,
                "url": url,
                "error": page_data.get("error", "Unknown error"),
                "links": []
            }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "links": []
        }
