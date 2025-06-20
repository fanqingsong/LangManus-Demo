"""LangGraph workflow for LangManus Demo."""

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
        prompt = prompt_template.load_prompt("coordinator")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=state["task"])
        ]
        
        response = basic_llm.invoke(messages)
        
        state["messages"].append({
            "agent": "coordinator",
            "content": response.content,
            "timestamp": "now"
        })
        
        state["current_step"] = "planner"
        return state
        
    except Exception as e:
        logger.error(f"Error in coordinator node: {e}")
        state["error"] = str(e)
        return state


def planner_node(state: WorkflowState) -> WorkflowState:
    """Planner agent node."""
    try:
        prompt = prompt_template.load_prompt("planner")
        
        if not reasoning_llm:
            state["error"] = "Reasoning LLM not configured"
            return state
            
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Create a plan for: {state['task']}")
        ]
        
        response = reasoning_llm.invoke(messages)
        
        state["messages"].append({
            "agent": "planner",
            "content": response.content,
            "timestamp": "now"
        })
        
        state["current_step"] = "researcher"
        return state
        
    except Exception as e:
        logger.error(f"Error in planner node: {e}")
        state["error"] = str(e)
        return state


def researcher_node(state: WorkflowState) -> WorkflowState:
    """Researcher agent node."""
    try:
        prompt = prompt_template.load_prompt("researcher")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        # Find trending repository
        repo_url = find_trending_repo()
        state["repo_url"] = repo_url
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"I found a trending repository: {repo_url}")
        ]
        
        response = basic_llm.invoke(messages)
        
        state["messages"].append({
            "agent": "researcher", 
            "content": f"Found trending repo: {repo_url}\n\nAnalysis: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "browser"
        return state
        
    except Exception as e:
        logger.error(f"Error in researcher node: {e}")
        state["error"] = str(e)
        return state


def browser_node(state: WorkflowState) -> WorkflowState:
    """Browser agent node."""
    try:
        prompt = prompt_template.load_prompt("browser")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        # Scrape GitHub activity
        repo_data = scrape_github_activity(state["repo_url"])
        state["repo_data"] = repo_data
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Scraped data from {state['repo_url']}: {len(repo_data.get('commits', []))} commits found")
        ]
        
        response = basic_llm.invoke(messages)
        
        state["messages"].append({
            "agent": "browser",
            "content": f"Scraped GitHub data: {len(repo_data.get('commits', []))} commits\n\nAnalysis: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "coder"
        return state
        
    except Exception as e:
        logger.error(f"Error in browser node: {e}")
        state["error"] = str(e)
        return state


def coder_node(state: WorkflowState) -> WorkflowState:
    """Coder agent node."""
    try:
        prompt = prompt_template.load_prompt("coder")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
        # Analyze code activity
        analysis, chart_paths = analyze_code_activity(state["repo_data"])
        state["analysis"] = analysis
        state["chart_paths"] = chart_paths
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"Generated analysis and {len(chart_paths)} charts for repository activity")
        ]
        
        response = basic_llm.invoke(messages)
        
        state["messages"].append({
            "agent": "coder",
            "content": f"Generated {len(chart_paths)} charts and analysis\n\nInsights: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "reporter"
        return state
        
    except Exception as e:
        logger.error(f"Error in coder node: {e}")
        state["error"] = str(e)
        return state


def reporter_node(state: WorkflowState) -> WorkflowState:
    """Reporter agent node."""
    try:
        prompt = prompt_template.load_prompt("reporter")
        
        if not basic_llm:
            state["error"] = "Basic LLM not configured"
            return state
            
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
                f"- **Stars:** {metadata.get('stars', 0)}",
                f"- **Forks:** {metadata.get('forks', 0)}",
                f""
            ])
        
        report_parts.extend([
            f"## 📝 Recent Commits:",
            f""
        ])
        
        for commit in repo_data.get('commits', [])[:10]:
            report_parts.append(f"- {commit}")
            
        report_parts.extend([
            f"",
            f"## 🔍 Analysis:",
            f""
        ])
        
        for line in analysis:
            report_parts.append(line)
            
        if chart_paths:
            report_parts.extend([
                f"",
                f"## 📊 Generated Charts:",
                f""
            ])
            for chart_path in chart_paths:
                chart_name = chart_path.split('/')[-1].replace('_', ' ').replace('.png', '').title()
                report_parts.append(f"- {chart_name}: `{chart_path}`")
        
        report = "\n".join(report_parts)
        state["report"] = report
        
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content="Generated comprehensive repository analysis report")
        ]
        
        response = basic_llm.invoke(messages)
        
        state["messages"].append({
            "agent": "reporter",
            "content": f"Generated final report\n\nSummary: {response.content}",
            "timestamp": "now"
        })
        
        state["current_step"] = "complete"
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