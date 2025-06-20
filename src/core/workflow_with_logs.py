"""LangGraph workflow for LangManus Demo with detailed logging."""

from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.llm import basic_llm, reasoning_llm
from src.prompts.template import prompt_template
from src.tools.github_tools import find_trending_repo, scrape_github_activity
from src.tools.analysis_tools import analyze_code_activity
import logging

logger = logging.getLogger(__name__)


class WorkflowState(TypedDict):
    """State structure for the workflow."""
    messages: List[Dict[str, Any]]
    task: str
    current_step: str
    repo_url: str
    repo_data: Dict[str, Any]
    analysis: List[str]
    chart_paths: List[str]
    report: str
    error: str


def coordinator_node(state: WorkflowState) -> WorkflowState:
    """Coordinator agent node."""
    try:
        print("🎯 [COORDINATOR] Starting task coordination...")
        logger.info("🎯 Coordinator Agent: Analyzing task and setting up workflow")
        
        prompt = prompt_template.load_prompt("coordinator")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        print(f"📋 Task: {state['task']}")
        logger.info(f"Task to coordinate: {state['task']}")
            
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=state["task"])
        ]
        
        print("💭 Coordinator is analyzing the task...")
        response = basic_llm.invoke(messages)
        
        print(f"✅ [COORDINATOR] Strategy:")
        print("-" * 30)
        print(response.content)
        print("-" * 30)
        logger.info(f"Coordinator strategy established: {response.content[:200]}")
        
        state["messages"].append({
            "agent": "coordinator",
            "content": response.content,
            "timestamp": "now"
        })
        
        state["current_step"] = "planner"
        print("➡️  Handing off to Planner Agent...")
        return state
        
    except Exception as e:
        logger.error(f"Error in coordinator node: {e}")
        state["error"] = str(e)
        return state


def planner_node(state: WorkflowState) -> WorkflowState:
    """Planner agent node."""
    try:
        print("\n📋 [PLANNER] Creating execution plan...")
        logger.info("📋 Planner Agent: Developing detailed execution strategy")
        
        prompt = prompt_template.load_prompt("planner")
        
        if not reasoning_llm:
            state["error"] = "Reasoning LLM not configured"
            return state
            
        print("🔍 Analyzing task requirements...")
        logger.info(f"Planning for task: {state['task']}")
            
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Create a plan for: {state['task']}")
        ]
        
        print("🧠 Planner is thinking through the strategy...")
        response = reasoning_llm.invoke(messages)
        
        print(f"✅ [PLANNER] Plan created:")
        print("-" * 50)
        print(response.content)
        print("-" * 50)
        logger.info(f"Execution plan established: {response.content[:200]}")
        
        state["messages"].append({
            "agent": "planner",
            "content": response.content,
            "timestamp": "now"
        })
        
        state["current_step"] = "researcher"
        print("➡️  Handing off to Researcher Agent...")
        return state
        
    except Exception as e:
        logger.error(f"Error in planner node: {e}")
        state["error"] = str(e)
        return state


def researcher_node(state: WorkflowState) -> WorkflowState:
    """Researcher agent node."""
    try:
        print("\n🔍 [RESEARCHER] Starting research phase...")
        logger.info("🔍 Researcher Agent: Gathering data and insights")
        
        prompt = prompt_template.load_prompt("researcher")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        print("📡 Finding trending repository...")
        # Find trending repository
        repo_url = find_trending_repo()
        state["repo_url"] = repo_url
        print(f"🎯 Found target repository: {repo_url}")
        logger.info(f"Found target URL: {repo_url}")
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"I found a trending repository: {repo_url}")
        ]
        
        print("💭 Researcher is analyzing the repository...")
        response = basic_llm.invoke(messages)
        
        print(f"✅ [RESEARCHER] Research complete. Found: {repo_url}")
        logger.info(f"Research phase completed")
        
        state["messages"].append({
            "agent": "researcher", 
            "content": f"Found trending repo: {repo_url}\n\nAnalysis: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "browser"
        print("➡️  Handing off to Browser Agent...")
        return state
        
    except Exception as e:
        logger.error(f"Error in researcher node: {e}")
        state["error"] = str(e)
        return state


def browser_node(state: WorkflowState) -> WorkflowState:
    """Browser agent node."""
    try:
        print("\n🌐 [BROWSER] Starting web data collection...")
        logger.info("🌐 Browser Agent: Collecting web-based information")
        
        prompt = prompt_template.load_prompt("browser")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        print(f"🎯 Target: {state['repo_url']}")
        print("📡 Scraping GitHub activity...")
        # Scrape GitHub activity
        repo_data = scrape_github_activity(state["repo_url"])
        state["repo_data"] = repo_data
        print(f"📊 Collected data: {len(repo_data.get('commits', []))} commits")
        logger.info(f"Scraped data from {state['repo_url']}")
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Scraped data from {state['repo_url']}: {len(repo_data.get('commits', []))} commits found")
        ]
        
        print("💭 Browser is analyzing the collected data...")
        response = basic_llm.invoke(messages)
        
        print(f"✅ [BROWSER] Web collection complete. Total commits: {len(repo_data.get('commits', []))}")
        logger.info(f"Browser phase completed with {len(repo_data.get('commits', []))} commits")
        
        state["messages"].append({
            "agent": "browser",
            "content": f"Scraped GitHub data: {len(repo_data.get('commits', []))} commits\n\nAnalysis: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "coder"
        print("➡️  Handing off to Coder Agent...")
        return state
        
    except Exception as e:
        logger.error(f"Error in browser node: {e}")
        state["error"] = str(e)
        return state


def coder_node(state: WorkflowState) -> WorkflowState:
    """Coder agent node."""
    try:
        print("\n💻 [CODER] Starting analysis and code generation...")
        logger.info("💻 Coder Agent: Processing data and generating insights")
        
        prompt = prompt_template.load_prompt("coder")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        print(f"📊 Processing {len(state['repo_data'].get('commits', []))} commits...")
        print("🔧 Using data analysis tools...")
        # Analyze code activity
        analysis, chart_paths = analyze_code_activity(state["repo_data"])
        state["analysis"] = analysis
        state["chart_paths"] = chart_paths
        print(f"✨ Generated {len(chart_paths)} visualizations/artifacts")
        logger.info(f"Generated {len(chart_paths)} artifacts")
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Generated analysis and {len(chart_paths)} charts for repository activity")
        ]
        
        print("💭 Coder is analyzing patterns and generating insights...")
        response = basic_llm.invoke(messages)
        
        print(f"✅ [CODER] Analysis complete. Generated {len(chart_paths)} artifacts")
        print("📝 Generated Insights:")
        print("-" * 40)
        print(response.content)
        print("-" * 40)
        logger.info(f"Coder phase completed with {len(chart_paths)} artifacts")
        
        state["messages"].append({
            "agent": "coder",
            "content": f"Generated {len(chart_paths)} charts and analysis\n\nInsights: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "reporter"
        print("➡️  Handing off to Reporter Agent...")
        return state
        
    except Exception as e:
        logger.error(f"Error in coder node: {e}")
        state["error"] = str(e)
        return state


def reporter_node(state: WorkflowState) -> WorkflowState:
    """Reporter agent node."""
    try:
        print("\n📊 [REPORTER] Generating comprehensive report...")
        logger.info("📊 Reporter Agent: Compiling final analysis report")
        
        prompt = prompt_template.load_prompt("reporter")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        print("📋 Gathering report components...")
        print(f"   • Repository: {state['repo_url']}")
        print(f"   • Commits analyzed: {len(state['repo_data'].get('commits', []))}")
        print(f"   • Generated charts: {len(state['chart_paths'])}")
        
        # Generate report
        repo_data = state["repo_data"]
        analysis = state["analysis"]
        chart_paths = state["chart_paths"]
        
        # Create comprehensive report
        report_parts = [
            f"# 🧠 GitHub Repository Analysis",
            f"",
            f"## 🔗 Repository: [{state['repo_url']}]({state['repo_url']})",
            f"",
            f"**Repository Metadata:**"
        ]
        
        metadata = repo_data.get('metadata', {})
        if metadata:
            report_parts.extend([
                f"- **Name:** {metadata.get('name', 'N/A')}",
                f"- **Description:** {metadata.get('description', 'N/A')}",
                f"- **Language:** {metadata.get('language', 'N/A')}",
                f"- **Stars:** {metadata.get('stargazers_count', 'N/A')}",
                f"- **Forks:** {metadata.get('forks_count', 'N/A')}",
                f""
            ])
        
        # Add recent commits
        commits = repo_data.get('commits', [])
        if commits:
            report_parts.extend([
                f"## 📝 Recent Commits:",
                f""
            ])
            for commit in commits[:10]:  # Show last 10 commits
                report_parts.append(f"- [{commit.get('sha', 'N/A')[:7]}] {commit.get('message', 'N/A')}")
            report_parts.append("")
        
        # Add analysis results
        if analysis:
            report_parts.extend([
                f"## 🔍 Analysis:",
                f""
            ])
            for item in analysis:
                report_parts.append(item)
            report_parts.append("")
        
        # Add chart information
        if chart_paths:
            report_parts.extend([
                f"## 📊 Generated Charts:",
                f""
            ])
            for chart_path in chart_paths:
                report_parts.append(f"- {chart_path}")
            report_parts.append("")
        
        # Generate final report
        report = "\n".join(report_parts)
        state["report"] = report
        
        print("💭 Reporter is synthesizing the final report...")
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Generate a comprehensive report for the analysis of {state['repo_url']}")
        ]
        
        response = basic_llm.invoke(messages)
        
        print(f"✅ [REPORTER] Report complete ({len(report)} characters)")
        logger.info(f"Reporter generated final report with {len(report)} characters")
        
        state["messages"].append({
            "agent": "reporter",
            "content": "Final report generated",
            "timestamp": "now"
        })
        
        state["current_step"] = "complete"
        print("\n🎉 [WORKFLOW] All agents completed successfully!")
        return state
        
    except Exception as e:
        logger.error(f"Error in reporter node: {e}")
        state["error"] = str(e)
        return state


def create_workflow() -> StateGraph:
    """Create the LangGraph workflow.
    
    Returns:
        StateGraph: Configured workflow graph
    """
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("coordinator", coordinator_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("browser", browser_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("reporter", reporter_node)
    
    # Add edges
    workflow.add_edge(START, "coordinator")
    workflow.add_edge("coordinator", "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "browser")
    workflow.add_edge("browser", "coder")
    workflow.add_edge("coder", "reporter")
    workflow.add_edge("reporter", END)
    
    return workflow.compile()


def create_github_workflow() -> StateGraph:
    """Create workflow with GitHub tools injected.
    
    This is a convenience function that demonstrates how to inject
    business-specific tools into the generic workflow.
    """
    # Import GitHub tools only when needed
    from src.tools.github_tools import find_trending_repo, scrape_github_activity
    from src.tools.analysis_tools import analyze_code_activity
    
    workflow = create_workflow()
    
    # This workflow pre-configures the GitHub tools
    # In practice, tools would be injected at runtime
    return workflow 