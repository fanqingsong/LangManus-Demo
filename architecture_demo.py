#!/usr/bin/env python3
"""
LangManus Architecture Demo - Clean Framework Design

This script demonstrates the key architectural principles of the refactored LangManus framework:
1. Generic, business-agnostic prompts
2. Dynamic tool injection for business logic
3. Clean separation between framework and domain-specific code
"""

def demo_prompt_comparison():
    """Show the difference between business-specific and generic prompts."""
    print("🎯 === Prompt Design Comparison ===\n")
    
    print("❌ BEFORE (Business Logic in Prompts):")
    print("─" * 50)
    print("""
# Researcher Agent (OLD)
You are a GitHub repository analyst specializing in finding trending Python projects.

## Your Responsibilities  
1. Find trending repositories on GitHub
2. Analyze commit patterns and GitHub activity
3. Extract GitHub-specific metadata
4. Focus on Python repositories with high stars

## Available Tools
- GitHub API for repository data
- GitHub trending pages access
- Repository commit analysis

## Instructions
- Always search GitHub trending
- Focus on Python repositories
- Generate GitHub-specific reports
""")
    
    print("\n✅ AFTER (Generic Framework + Tool Injection):")
    print("─" * 50)
    print("""
# Researcher Agent (NEW)
You are a researcher specializing in information gathering.

## Your Responsibilities
1. Information Gathering: Collect data from various sources
2. Research: Conduct thorough research on specified topics  
3. Data Collection: Use available tools to gather relevant information
4. Analysis: Analyze collected information and identify key insights

## Available Tools
You have access to various tools for research. Use them appropriately based on task requirements.

## Instructions
- Always provide accurate information
- Use available tools effectively
- Present findings clearly and organized
""")


def demo_tool_injection():
    """Demonstrate how business logic is moved to tools."""
    print("\n🔧 === Tool Injection Architecture ===\n")
    
    # Simulate generic framework
    class GenericAgent:
        def __init__(self, name, tools=None):
            self.name = name
            self.tools = tools or {}
            
        def execute_task(self, task):
            print(f"[{self.name}] Executing: {task}")
            
            # Use injected tools if available
            if "find_data" in self.tools:
                data = self.tools["find_data"]()
                print(f"[{self.name}] Using injected tool: {data}")
            
            if "analyze_data" in self.tools:
                result = self.tools["analyze_data"]({"sample": "data"})
                print(f"[{self.name}] Analysis result: {result}")
            
            return f"Task completed by {self.name}"
    
    # Business-specific tools (GitHub domain)
    def github_find_data():
        return "Found trending GitHub repository: https://github.com/example/repo"
    
    def github_analyze_data(data):
        return "GitHub analysis: 150 commits, 25 contributors, Python language"
    
    # Business-specific tools (Finance domain)  
    def finance_find_data():
        return "Found stock data: AAPL $150.25 (+2.5%)"
    
    def finance_analyze_data(data):
        return "Financial analysis: Bullish trend, strong fundamentals"
    
    print("🧠 Generic Framework Demo:")
    print("─" * 30)
    
    # Same generic agent, different business domains
    github_tools = {
        "find_data": github_find_data,
        "analyze_data": github_analyze_data
    }
    
    finance_tools = {
        "find_data": finance_find_data, 
        "analyze_data": finance_analyze_data
    }
    
    # GitHub analysis using generic framework
    github_agent = GenericAgent("Researcher", github_tools)
    github_agent.execute_task("Analyze repository trends")
    
    print()
    
    # Finance analysis using same generic framework
    finance_agent = GenericAgent("Researcher", finance_tools)  
    finance_agent.execute_task("Analyze market trends")


def demo_architecture_benefits():
    """Show the benefits of the new architecture."""
    print("\n🏆 === Architecture Benefits ===\n")
    
    benefits = [
        {
            "aspect": "Prompt Reusability",
            "old": "New domain = New prompts",
            "new": "Same prompts for all domains"
        },
        {
            "aspect": "Code Maintenance", 
            "old": "Change prompts for each domain",
            "new": "Add tools only"
        },
        {
            "aspect": "Testing",
            "old": "Test entire agent system",
            "new": "Test tools independently"
        },
        {
            "aspect": "Deployment",
            "old": "Deploy different agent versions",
            "new": "Deploy framework + inject tools"
        },
        {
            "aspect": "Extensibility",
            "old": "Modify core framework code",
            "new": "Create new tool modules"
        }
    ]
    
    print("│ Aspect             │ Old Approach              │ New Approach              │")
    print("├────────────────────┼───────────────────────────┼───────────────────────────┤")
    
    for benefit in benefits:
        aspect = benefit["aspect"].ljust(18)
        old = benefit["old"].ljust(25)
        new = benefit["new"].ljust(25)
        print(f"│ {aspect} │ {old} │ {new} │")


def demo_usage_patterns():
    """Show different usage patterns for the framework."""
    print("\n🚀 === Usage Patterns ===\n")
    
    print("1️⃣  Generic Analysis (No Domain Tools):")
    print("─" * 40)
    print("""
from langmanus import LangManusAgent

agent = LangManusAgent(
    task="Analyze artificial intelligence trends"
)
result = agent.run()  # Uses generic prompts only
""")
    
    print("\n2️⃣  Custom Business Domain:")
    print("─" * 40)
    print("""
# Define your business tools
def analyze_medical_data(data):
    return "Medical analysis complete"

def fetch_patient_records(id):
    return {"patient": id, "diagnosis": "..."}

# Inject into generic framework
medical_tools = {
    "analyze_medical_data": analyze_medical_data,
    "fetch_patient_records": fetch_patient_records
}

agent = LangManusAgent(
    task="Analyze patient medical history",
    tools=medical_tools
)
result = agent.run()
""")
    
    print("\n3️⃣  Pre-configured Domain Agent:")
    print("─" * 40)
    print("""
from langmanus import GitHubAnalysisAgent

# Convenience class with GitHub tools pre-injected
agent = GitHubAnalysisAgent()
result = agent.run()  # Same framework, GitHub tools injected
""")


def main():
    """Run the complete architecture demonstration."""
    print("🏗️ === LangManus Architecture Refactoring Demo ===")
    print("Demonstrating clean separation between framework and business logic\n")
    
    demo_prompt_comparison()
    demo_tool_injection()
    demo_architecture_benefits()
    demo_usage_patterns()
    
    print("\n🎉 === Summary ===")
    print("✅ Prompts are now generic and business-agnostic")
    print("✅ Business logic is contained in injectable tools")
    print("✅ Framework can work with any domain")
    print("✅ Clean separation of concerns achieved")
    print("✅ Easy to extend to new business domains")
    
    print("\n💡 Key Insight:")
    print("   LangManus should be a GENERIC framework")
    print("   Business domains provide TOOLS")
    print("   Tools are INJECTED at runtime")
    print("   Framework stays DOMAIN-AGNOSTIC")


if __name__ == "__main__":
    main() 