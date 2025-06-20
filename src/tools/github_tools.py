"""GitHub-related tools for repository analysis."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import logging
from src.config.env import GITHUB_TOKEN
from src.config.tools import GITHUB_MAX_COMMITS

logger = logging.getLogger(__name__)


def find_trending_repo() -> str:
    """Find a trending Python repository on GitHub.
    
    Returns:
        str: URL of a trending repository
    """
    try:
        url = "https://github.com/trending/python"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_element = soup.select_one('article h2 a')
        
        if repo_element:
            repo_path = repo_element['href'].strip()
            return f"https://github.com{repo_path}"
        else:
            # Fallback to a known popular repository
            return "https://github.com/python/cpython"
            
    except Exception as e:
        logger.error(f"Error finding trending repo: {e}")
        # Fallback to a known popular repository
        return "https://github.com/python/cpython"


def get_repo_metadata(repo_url: str) -> Dict[str, Any]:
    """Get metadata for a GitHub repository.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Dict containing repository metadata
    """
    try:
        headers = {}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
            
        user_repo = "/".join(repo_url.split('/')[-2:])
        api_url = f"https://api.github.com/repos/{user_repo}"
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            'name': data.get('name', ''),
            'full_name': data.get('full_name', ''),
            'description': data.get('description', ''),
            'language': data.get('language', ''),
            'stars': data.get('stargazers_count', 0),
            'forks': data.get('forks_count', 0),
            'issues': data.get('open_issues_count', 0),
            'created_at': data.get('created_at', ''),
            'updated_at': data.get('updated_at', ''),
            'url': repo_url
        }
        
    except Exception as e:
        logger.error(f"Error getting repo metadata: {e}")
        return {
            'name': repo_url.split('/')[-1],
            'url': repo_url,
            'error': str(e)
        }


def scrape_github_activity(repo_url: str) -> Dict[str, Any]:
    """Scrape GitHub repository activity data.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Dict containing repository activity data
    """
    try:
        headers = {}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        user_repo = "/".join(repo_url.split('/')[-2:])
        api_url = f"https://api.github.com/repos/{user_repo}/commits"

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        commits = []
        commit_dates = []

        for item in data[:GITHUB_MAX_COMMITS]:
            try:
                message = item['commit']['message']
                author = item['commit']['author']['name']
                date = item['commit']['author']['date']
                sha = item['sha'][:7]

                commits.append(f"[{sha}] {message} — {author} @ {date}")
                commit_dates.append(date)
            except KeyError as e:
                logger.warning(f"Missing key in commit data: {e}")
                continue

        # Get repository metadata
        metadata = get_repo_metadata(repo_url)

        return {
            'repo_url': repo_url,
            'commits': commits,
            'commit_dates': commit_dates,
            'metadata': metadata
        }
        
    except Exception as e:
        logger.error(f"Error scraping GitHub activity: {e}")
        return {
            'repo_url': repo_url,
            'commits': [],
            'commit_dates': [],
            'error': str(e)
        } 