"""Main entry point for LangManus Demo."""

from src.main_app import LangManusAgent

if __name__ == '__main__':
    # Use the new LangManus-powered agent
    # agent = LangManusAgent(task="Find a popular open-source project updated recently and summarize its new features with examples and charts.")
    agent = LangManusAgent(task="Find a popular open-source project updated recently and summarize its new features with examples and charts, finally save the summary into file.")
    result = agent.run()
    
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
    else:
        print("✅ Analysis completed!")
        print("\n" + "="*60)
        print(result.get("report", "No report generated"))
        print("="*60)
        
        chart_paths = result.get("chart_paths", [])
        if chart_paths:
            print(f"\n📊 Generated {len(chart_paths)} charts:")
            for path in chart_paths:
                print(f"  - {path}")