"""Search tools for web search and information retrieval."""

from typing import List, Dict, Any, Optional
import logging
from src.config.env import TAVILY_API_KEY
from src.config.tools import TAVILY_MAX_RESULTS

logger = logging.getLogger(__name__)


def tavily_search(query: str, max_results: int = None) -> List[Dict[str, Any]]:
    """Search the web using Tavily API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results (defaults to config value)
        
    Returns:
        List of search results
    """
    if not TAVILY_API_KEY:
        logger.warning("Tavily API key not configured")
        return []
        
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=TAVILY_API_KEY)
        max_results = max_results or TAVILY_MAX_RESULTS
        
        response = client.search(
            query=query,
            max_results=max_results,
            include_answer=True,
            include_raw_content=False
        )
        
        return response.get('results', [])
        
    except ImportError:
        logger.error("Tavily package not installed")
        return []
    except Exception as e:
        logger.error(f"Error during Tavily search: {e}")
        return []


def search_github_repos(query: str, language: str = "python") -> List[Dict[str, Any]]:
    """Search for GitHub repositories.
    
    Args:
        query: Search query
        language: Programming language filter
        
    Returns:
        List of repository information
    """
    try:
        search_query = f"{query} language:{language} trending"
        results = tavily_search(search_query)
        
        # Filter results to GitHub repositories
        github_repos = []
        for result in results:
            url = result.get('url', '')
            if 'github.com' in url and '/blob/' not in url and '/issues/' not in url:
                github_repos.append({
                    'title': result.get('title', ''),
                    'url': url,
                    'content': result.get('content', ''),
                    'score': result.get('score', 0)
                })
                
        return github_repos
        
    except Exception as e:
        logger.error(f"Error searching GitHub repos: {e}")
        return [] 