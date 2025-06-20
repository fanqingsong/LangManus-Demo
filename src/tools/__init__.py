"""Tools for LangManus Demo."""

from .github_tools import (
    find_trending_repo,
    scrape_github_activity,
    get_repo_metadata
)
from .analysis_tools import (
    analyze_code_activity,
    categorize_commit,
    generate_charts
)
from .search_tools import (
    tavily_search,
    search_github_repos
)

__all__ = [
    "find_trending_repo",
    "scrape_github_activity", 
    "get_repo_metadata",
    "analyze_code_activity",
    "categorize_commit",
    "generate_charts",
    "tavily_search",
    "search_github_repos"
] 