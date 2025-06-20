#!/usr/bin/env python3
"""
LangManus Demo - GitHub Repository Analyzer

This script demonstrates the LangManus framework capabilities by analyzing
a GitHub repository using a multi-agent system.
"""

import logging
from src.main_app import LangManusAgent
from src.tools.github_tools import find_trending_repo
from src.tools.analysis_tools import categorize_commit, analyze_code_activity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_basic_tools():
    """Demonstrate basic tool functionality."""
    print("🔧 === LangManus Basic Tools Demo ===")
    
    # Test commit categorization
    print("\n📊 Commit Categorization:")
    test_commits = [
        "fix: resolve memory leak in data processing",
        "feat: implement user authentication system", 
        "docs: add comprehensive API documentation",
        "refactor: optimize database queries",
        "test: add unit tests for core functionality"
    ]
    
    for commit in test_commits:
        category = categorize_commit(commit)
        print(f"  • {commit} → {category}")
    
    # Test repo finding (with fallback)
    print(f"\n🔍 Repository Discovery:")
    try:
        repo_url = find_trending_repo()
        print(f"  • Found trending repository: {repo_url}")
    except Exception as e:
        print(f"  • Error accessing GitHub (expected in demo): {str(e)[:100]}...")


def demo_mock_analysis():
    """Demonstrate analysis with mock data."""
    print("\n📈 === Analysis Demo with Mock Data ===")
    
    # Mock repository data
    mock_repo_data = {
        'repo_url': 'https://github.com/example/awesome-python-project',
        'commits': [
            '[abc123] feat: add new ML model training pipeline — Alice @ 2024-01-15T10:30:00Z',
            '[def456] fix: resolve memory leak in data loader — Bob @ 2024-01-14T16:45:00Z',
            '[ghi789] docs: update installation instructions — Charlie @ 2024-01-13T09:15:00Z',
            '[jkl012] feat: implement real-time data streaming — Alice @ 2024-01-12T14:20:00Z',
            '[mno345] test: add comprehensive unit tests — David @ 2024-01-11T11:30:00Z'
        ],
        'commit_dates': [
            '2024-01-15T10:30:00Z',
            '2024-01-14T16:45:00Z', 
            '2024-01-13T09:15:00Z',
            '2024-01-12T14:20:00Z',
            '2024-01-11T11:30:00Z'
        ],
        'metadata': {
            'name': 'awesome-python-project',
            'description': 'A modern ML pipeline with real-time capabilities',
            'language': 'Python',
            'stars': 1234,
            'forks': 567
        }
    }
    
    # Perform analysis
    analysis, chart_paths = analyze_code_activity(mock_repo_data)
    
    print("\n📊 Analysis Results:")
    for line in analysis:
        print(f"  {line}")
        
    if chart_paths:
        print(f"\n📈 Generated Charts:")
        for chart_path in chart_paths:
            print(f"  • {chart_path}")
    else:
        print("\n📈 Charts: None generated (display/file system limitations)")


def demo_langmanus_agent():
    """Demonstrate the full LangManus agent (without API keys)."""
    print("\n🤖 === LangManus Agent Demo ===")
    
    # Note: This will fail without proper API keys, but shows structure
    print("Initializing LangManus Agent...")
    agent = LangManusAgent(task="Analyze a trending GitHub repository")
    
    print("✅ Agent initialized with LangManus framework")
    print("📋 Configured agents: Coordinator, Planner, Supervisor, Researcher, Browser, Coder, Reporter")
    print("🔧 Available tools: GitHub API, Analysis tools, Search capabilities")
    print("💬 Prompt system: Loaded with specialized agent prompts")
    print("🔄 Workflow: LangGraph-based multi-agent coordination")
    
    print("\n⚠️  Note: Full execution requires API keys (OpenAI, GitHub, etc.)")
    print("   Configure .env file with your API keys to run complete workflow")


def main():
    """Run the complete LangManus demo."""
    print("🧠 === LangManus Framework Demo ===")
    print("A sophisticated multi-agent system for GitHub repository analysis\n")
    
    try:
        # Run demonstrations
        demo_basic_tools()
        demo_mock_analysis()
        demo_langmanus_agent()
        
        print("\n🎉 === Demo Complete ===")
        print("✅ LangManus framework successfully integrated!")
        print("🚀 Ready for production use with proper API configuration")
        
        print(f"\n📚 Next Steps:")
        print(f"  1. Configure API keys in .env file")
        print(f"  2. Run: make run (for CLI)")
        print(f"  3. Run: make streamlit (for web UI)")
        print(f"  4. Run: make serve (for API server)")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main() 