"""Tools for LangManus Demo."""

# Core tools (no external dependencies)
from .python_tools import (
    execute_python_code,
    execute_repl_code,
    install_package,
    run_shell_command,
    check_python_environment,
    reset_repl
)
from .file_tools import (
    read_file,
    write_file,
    save_report
)
from .bash_tool import (
    execute_bash_command,
    execute_bash_script
)
from .decorators import (
    retry,
    timeout,
    log_execution,
    safe_execute
)

# Tools requiring external dependencies (optional import)
try:
    from .github_tools import (
        find_trending_repo,
        scrape_github_activity,
        get_repo_metadata
    )
    _github_tools_available = True
except ImportError:
    find_trending_repo = None
    scrape_github_activity = None
    get_repo_metadata = None
    _github_tools_available = False

try:
    from .analysis_tools import (
        analyze_code_activity,
        categorize_commit,
        generate_charts
    )
    _analysis_tools_available = True
except ImportError:
    analyze_code_activity = None
    categorize_commit = None
    generate_charts = None
    _analysis_tools_available = False

try:
    from .search_tools import (
        tavily_search,
        search_github_repos
    )
    _search_tools_available = True
except ImportError:
    tavily_search = None
    search_github_repos = None
    _search_tools_available = False

try:
    from .browser_tools import (
        fetch_webpage,
        get_page_metadata
    )
    _browser_tools_available = True
except ImportError:
    fetch_webpage = None
    get_page_metadata = None
    _browser_tools_available = False

try:
    from .crawl import (
        crawl_single_page,
        extract_links_from_page
    )
    _crawl_tools_available = True
except ImportError:
    crawl_single_page = None
    extract_links_from_page = None
    _crawl_tools_available = False

__all__ = [
    # GitHub tools
    "find_trending_repo",
    "scrape_github_activity", 
    "get_repo_metadata",
    
    # Analysis tools
    "analyze_code_activity",
    "categorize_commit",
    "generate_charts",
    
    # Search tools
    "tavily_search",
    "search_github_repos",
    
    # Python execution tools
    "execute_python_code",
    "execute_repl_code",
    "install_package",
    "run_shell_command",
    "check_python_environment",
    "reset_repl",
    
    # File management tools
    "read_file",
    "write_file",
    "save_report",
    
    # Browser tools
    "fetch_webpage",
    "get_page_metadata",
    
    # Bash tools
    "execute_bash_command",
    "execute_bash_script",
    
    # Crawling tools
    "crawl_single_page",
    "extract_links_from_page",
    
    # Decorator utilities
    "retry",
    "timeout",
    "log_execution",
    "safe_execute"
] 


def get_github_tools():
    """Get GitHub-specific tools."""
    if not _github_tools_available:
        print("⚠️ GitHub tools not available - install: pip install beautifulsoup4 requests")
        return {}
    return {
        "find_trending_repo": find_trending_repo,
        "scrape_github_activity": scrape_github_activity,
        "get_repo_metadata": get_repo_metadata
    }


def get_analysis_tools():
    """Get analysis tools."""
    if not _analysis_tools_available:
        print("⚠️ Analysis tools not available - install: pip install matplotlib")
        return {}
    return {
        "analyze_code_activity": analyze_code_activity,
        "categorize_commit": categorize_commit,
        "generate_charts": generate_charts
    }


def get_search_tools():
    """Get search tools."""
    if not _search_tools_available:
        print("⚠️ Search tools not available - install: pip install tavily-python")
        return {}
    return {
        "tavily_search": tavily_search,
        "search_github_repos": search_github_repos
    }


def get_python_tools():
    """Get Python execution tools."""
    return {
        "execute_python_code": execute_python_code,
        "execute_repl_code": execute_repl_code,
        "install_package": install_package,
        "run_shell_command": run_shell_command,
        "check_python_environment": check_python_environment,
        "reset_repl": reset_repl
    }


def get_file_tools():
    """Get file management tools."""
    return {
        "read_file": read_file,
        "write_file": write_file,
        "save_report": save_report
    }


def get_bash_tools():
    """Get bash execution tools."""
    return {
        "execute_bash_command": execute_bash_command,
        "execute_bash_script": execute_bash_script
    }


def get_browser_tools():
    """Get browser tools."""
    if not _browser_tools_available:
        print("⚠️ Browser tools not available - install: pip install beautifulsoup4 requests")
        return {}
    return {
        "fetch_webpage": fetch_webpage,
        "get_page_metadata": get_page_metadata
    }


def get_crawl_tools():
    """Get web crawling tools."""
    if not _crawl_tools_available:
        print("⚠️ Crawl tools not available - install: pip install beautifulsoup4 requests")
        return {}
    return {
        "crawl_single_page": crawl_single_page,
        "extract_links_from_page": extract_links_from_page
    }


def get_decorator_tools():
    """Get decorator utilities."""
    return {
        "retry": retry,
        "timeout": timeout,
        "log_execution": log_execution,
        "safe_execute": safe_execute
    }


def get_available_tools():
    """Get all available tools based on installed dependencies."""
    tools = {}
    
    # Always available core tools
    tools.update(get_python_tools())
    tools.update(get_file_tools())
    tools.update(get_bash_tools())
    tools.update(get_decorator_tools())
    
    # Optional tools based on dependencies
    tools.update(get_github_tools())
    tools.update(get_analysis_tools())
    tools.update(get_search_tools())
    tools.update(get_browser_tools())
    tools.update(get_crawl_tools())
    
    return {k: v for k, v in tools.items() if v is not None}


def check_tool_availability():
    """Check and report tool availability."""
    availability = {
        "Core Tools": True,  # Always available
        "GitHub Tools": _github_tools_available,
        "Analysis Tools": _analysis_tools_available,
        "Search Tools": _search_tools_available,
        "Browser Tools": _browser_tools_available,
        "Crawl Tools": _crawl_tools_available
    }
    
    print("🔧 Tool Availability Status:")
    for category, available in availability.items():
        status = "✅" if available else "❌"
        print(f"   {status} {category}")
    
    if not all(availability.values()):
        print("\n💡 To install missing dependencies:")
        print("   pip install beautifulsoup4 requests matplotlib tavily-python")
    
    return availability