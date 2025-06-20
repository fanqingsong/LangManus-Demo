#!/usr/bin/env python3
"""
LangManus Demo - Generic Multi-Agent Framework

This script demonstrates the LangManus framework's generic design with dynamic tool injection.
It shows how business-specific tools (like GitHub tools) can be injected into the framework
without polluting the core agent prompts.
"""

import logging
from src.main_app import LangManusAgent, GitHubAnalysisAgent
from src.tools.github_tools import find_trending_repo
from src.tools.analysis_tools import categorize_commit, analyze_code_activity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_generic_framework():
    """Demonstrate the generic LangManus framework without business tools."""
    print("🧠 === Generic LangManus Framework Demo ===")
    
    # Create a generic agent without any business-specific tools
    generic_agent = LangManusAgent(
        task="Analyze the concept of artificial intelligence and its impact on society"
    )
    
    print(f"✅ Generic Agent Created")
    print(f"   Task: {generic_agent.task}")
    print(f"   Tools: {list(generic_agent.tools.keys()) if generic_agent.tools else 'None (generic framework)'}")
    print(f"   Prompts: Generic, business-agnostic agent prompts")
    
    # Note: This would work with any LLM configuration


def demo_tool_injection():
    """Demonstrate dynamic tool injection for specific business needs."""
    print("\n🔧 === Tool Injection Demo ===")
    
    # Define custom business tools
    def analyze_text(data):
        """Custom text analysis tool."""
        return ["Text analysis completed"], ["analysis_report.txt"]
    
    def fetch_data(source):
        """Custom data fetching tool."""
        return {"source": source, "data": "Sample data from " + source}
    
    # Also demonstrate using built-in tools
    from src.tools.python_tools import execute_python_code
    from src.tools.file_tools import write_file, save_report
    from src.tools.bash_tool import execute_bash_command
    from src.tools.crawl import crawl_single_page
    
    # Inject comprehensive tools into the framework
    custom_tools = {
        # Custom business tools
        "analyze_text": analyze_text,
        "fetch_data": fetch_data,
        
        # Built-in tools from LangManus
        "execute_python_code": execute_python_code,
        "write_file": write_file,
        "save_report": save_report,
        "execute_bash_command": execute_bash_command,
        "crawl_single_page": crawl_single_page
    }
    
    custom_agent = LangManusAgent(
        task="Analyze text data from various sources and save results",
        tools=custom_tools
    )
    
    print(f"✅ Custom Agent Created with Comprehensive Tool Injection")
    print(f"   Available tools: {list(custom_agent.tools.keys())}")
    print(f"   Framework: Same generic LangManus framework")
    print(f"   Prompts: Same generic prompts, tools provide business logic")
    print(f"   Built-in Tools: Python execution, file management, reporting")
    print(f"   Additional Tools: Bash execution, web crawling")


def demo_github_business_agent():
    """Demonstrate pre-configured GitHub business agent."""
    print("\n📊 === GitHub Business Agent Demo ===")
    
    # Create a GitHub-specific agent (convenience class)
    github_agent = GitHubAnalysisAgent()
    
    print(f"✅ GitHub Analysis Agent Created")
    print(f"   Task: {github_agent.task}")
    print(f"   Tools: {list(github_agent.tools.keys())}")
    print(f"   Framework: Same generic LangManus framework")
    print(f"   Business Logic: Provided by injected GitHub tools")
    
    # Test GitHub tools separately
    print(f"\n🔧 Testing GitHub Tools:")
    try:
        repo_url = find_trending_repo()
        print(f"   • GitHub tool working: {repo_url}")
    except Exception as e:
        print(f"   • GitHub tool demo (no API): {str(e)[:50]}...")


def demo_framework_architecture():
    """Demonstrate the clean architecture separation."""
    print("\n🏗️ === Framework Architecture Demo ===")
    
    print("📋 LangManus Architecture:")
    print("   ┌─────────────────────────────────────┐")
    print("   │        Generic Framework            │")
    print("   │  ┌─────────────────────────────┐    │")
    print("   │  │    Generic Prompts          │    │")
    print("   │  │  • Coordinator              │    │")
    print("   │  │  • Planner                  │    │")
    print("   │  │  • Researcher               │    │")
    print("   │  │  • Browser                  │    │")
    print("   │  │  • Coder                    │    │")
    print("   │  │  • Reporter                 │    │")
    print("   │  │  • File Manager             │    │")
    print("   │  └─────────────────────────────┘    │")
    print("   │                │                    │")
    print("   │        ┌───────▼──────┐             │")
    print("   │        │ Tool Injection│             │")
    print("   │        └───────┬──────┘             │")
    print("   └────────────────┼──────────────────────┘")
    print("                    │")
    print("   ┌────────────────▼──────────────────────┐")
    print("   │        Business Tools                 │")
    print("   │  • GitHub API Tools                   │")
    print("   │  • Python Execution Tools             │")
    print("   │  • Bash Execution Tools               │")
    print("   │  • File Management Tools              │")
    print("   │  • Web Crawling Tools                 │")
    print("   │  • Custom Business Tools              │")
    print("   └───────────────────────────────────────┘")
    
    print("\n✅ Key Design Principles:")
    print("   • Prompts are generic and business-agnostic")
    print("   • Business logic is contained in tools")
    print("   • Tools are injected dynamically at runtime")
    print("   • Framework can work with any domain-specific tools")
    print("   • Clean separation between framework and business logic")


def main():
    """Run the complete LangManus architecture demo."""
    print("🚀 === LangManus Framework Architecture Demo ===")
    print("Demonstrating generic framework design with dynamic tool injection\n")
    
    try:
        # Run demonstrations
        demo_generic_framework()
        demo_tool_injection()
        demo_github_business_agent()
        demo_framework_architecture()
        
        print("\n🎉 === Demo Complete ===")
        print("🏗️  Generic framework + Dynamic tool injection = Flexible AI system")
        
        print(f"\n📚 Key Benefits:")
        print(f"  • Framework remains domain-agnostic")
        print(f"  • Prompts are reusable across different business domains")
        print(f"  • Tools provide business-specific functionality")
        print(f"  • Easy to add new business domains without changing core framework")
        print(f"  • Clean separation of concerns")
        
        print(f"\n🔧 Usage Examples:")
        print(f"  • GitHub Analysis: GitHubAnalysisAgent()")
        print(f"  • Custom Business: LangManusAgent(tools=custom_tools)")
        print(f"  • Generic Analysis: LangManusAgent(task='analyze topic')")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main() 
