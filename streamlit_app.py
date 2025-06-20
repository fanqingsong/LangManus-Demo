"""Streamlit application for LangManus Demo."""

import streamlit as st
import os
from PIL import Image
from src.main_app import LangManusAgent

st.set_page_config(page_title="LangManus GitHub Analyzer", layout="wide")
st.title("🧠 LangManus GitHub Repo Analyzer")

st.markdown("""
This application uses the **LangManus framework** to analyze trending GitHub repositories.
It employs multiple specialized agents working together to provide comprehensive insights.
""")

# Sidebar with configuration
st.sidebar.header("Configuration")
st.sidebar.markdown("""
**LangManus Multi-Agent System:**
- 🎯 Coordinator
- 📋 Planner  
- 👑 Supervisor
- 🔍 Researcher
- 🌐 Browser
- 💻 Coder
- 📝 Reporter
""")

# Custom task input
custom_task = st.text_area(
    "Custom Task (optional):",
    value="Find a popular open-source project updated recently and summarize its new features with examples and charts.",
    height=100
)

if st.button("🔍 Run LangManus Analysis", type="primary"):
    with st.spinner("Running LangManus multi-agent workflow..."):
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize agent
            agent = LangManusAgent(task=custom_task)
            
            # Run analysis with progress updates
            status_text.text("🎯 Initializing coordinator...")
            progress_bar.progress(10)
            
            result = agent.run()
            
            if result.get("error"):
                st.error(f"❌ Analysis failed: {result['error']}")
            else:
                progress_bar.progress(100)
                status_text.text("✅ Analysis completed!")
                
                # Display results
                st.success("🎉 LangManus analysis completed successfully!")
                
                # Show repository information
                if result.get("repo_url"):
                    st.subheader("🔗 Analyzed Repository")
                    st.markdown(f"**Repository:** [{result['repo_url']}]({result['repo_url']})")
                
                # Display the report
                if result.get("report"):
                    st.subheader("📋 Analysis Report")
                    st.markdown(result["report"])
                
                # Display charts
                chart_paths = result.get("chart_paths", [])
                if chart_paths:
                    st.subheader("📊 Generated Charts")
                    
                    # Create columns for charts
                    cols = st.columns(min(len(chart_paths), 3))
                    
                    for i, chart_path in enumerate(chart_paths):
                        if os.path.exists(chart_path):
                            col_idx = i % len(cols)
                            with cols[col_idx]:
                                chart_name = os.path.basename(chart_path).replace('_', ' ').replace('.png', '').title()
                                st.image(
                                    Image.open(chart_path), 
                                    caption=chart_name,
                                    use_container_width=True
                                )
                        else:
                            st.warning(f"Chart file not found: {chart_path}")
                
                # Show agent messages
                messages = result.get("messages", [])
                if messages:
                    with st.expander("🤖 Agent Workflow Details"):
                        for msg in messages:
                            agent_name = msg.get("agent", "Unknown")
                            content = msg.get("content", "")
                            st.markdown(f"**{agent_name.title()}:** {content}")
                            st.divider()
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            progress_bar.progress(0)
            status_text.text("❌ Analysis failed")

else:
    st.info("👆 Click the button above to start the LangManus analysis workflow.")
    
    # Show example output
    st.subheader("🎯 What LangManus Does")
    st.markdown("""
    The LangManus framework coordinates multiple AI agents to:
    
    1. **🔍 Research** - Find trending Python repositories
    2. **🌐 Browse** - Scrape GitHub data and commit history  
    3. **💻 Code** - Analyze patterns and generate visualizations
    4. **📝 Report** - Create comprehensive markdown reports
    
    Each agent specializes in specific tasks and works together under the supervision
    of a coordinator and planner to deliver comprehensive analysis.
    """)

# Footer
st.markdown("---")
st.markdown("Powered by **LangManus Framework** - A community-driven AI automation platform")
