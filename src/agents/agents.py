"""LangManus agents implementation using create_react_agent.

This follows the official LangManus pattern where each agent is bound to specific tools
rather than passing tools through state.
"""

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

import src.tools.bash_tool as bash_tool
import src.tools.browser_tools as browser_tools
import src.tools.python_tools as python_tools
import src.tools.file_tools as file_tools
import src.tools.search_tools as search_tools
import src.tools.github_tools as github_tools
import src.tools.analysis_tools as analysis_tools

from src.core.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
import logging

logger = logging.getLogger(__name__)


def create_coordinator_agent():
    """Create coordinator agent with basic LLM and no tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["coordinator"])
        if not llm:
            logger.error("Failed to create LLM for coordinator agent")
            return None
            
        return create_react_agent(
            llm,
            tools=[],
            prompt="You are a Coordinator agent. Your role is to analyze the user's task and coordinate the workflow. Respond to the user input with a clear strategy.",
        )
    except Exception as e:
        logger.error(f"Error creating coordinator agent: {e}")
        return None


def create_planner_agent():
    """Create planner agent with reasoning LLM and no tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["planner"])
        if not llm:
            logger.error("Failed to create LLM for planner agent")
            return None
            
        return create_react_agent(
            llm,
            tools=[],
            prompt="You are a Planner agent. Your role is to create detailed execution plans for tasks. Respond to the user input with a structured plan.",
        )
    except Exception as e:
        logger.error(f"Error creating planner agent: {e}")
        return None


def create_researcher_agent():
    """Create researcher agent with search and crawling tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["researcher"])
        if not llm:
            logger.error("Failed to create LLM for researcher agent")
            return None
        
        tools = []
        try:
            if hasattr(search_tools, 'tavily_search'):
                tools.append(search_tools.tavily_search)
        except:
            pass
            
        try:
            if hasattr(github_tools, 'find_trending_repo'):
                tools.append(github_tools.find_trending_repo)
        except:
            pass
            
        return create_react_agent(
            llm,
            tools=tools,
            prompt="You are a Researcher agent. Your role is to gather information and data. Use available tools to research the topic.",
        )
    except Exception as e:
        logger.error(f"Error creating researcher agent: {e}")
        return None


def create_browser_agent():
    """Create browser agent with web browsing tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["browser"])
        if not llm:
            logger.error("Failed to create LLM for browser agent")
            return None
        
        tools = []
        try:
            if hasattr(browser_tools, 'fetch_webpage'):
                tools.append(browser_tools.fetch_webpage)
        except:
            pass
            
        try:
            if hasattr(github_tools, 'scrape_github_activity'):
                tools.append(github_tools.scrape_github_activity)
        except:
            pass
            
        return create_react_agent(
            llm,
            tools=tools,
            prompt="You are a Browser agent. Your role is to browse web pages and collect information. Use available tools to fetch web content.",
        )
    except Exception as e:
        logger.error(f"Error creating browser agent: {e}")
        return None


def create_coder_agent():
    """Create coder agent with Python and analysis tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["coder"])
        if not llm:
            logger.error("Failed to create LLM for coder agent")
            return None
        
        tools = []
        try:
            if hasattr(python_tools, 'execute_python_code'):
                tools.append(python_tools.execute_python_code)
        except:
            pass
            
        try:
            if hasattr(python_tools, 'execute_repl_code'):
                tools.append(python_tools.execute_repl_code)
        except:
            pass
            
        try:
            if hasattr(bash_tool, 'execute_bash_command'):
                tools.append(bash_tool.execute_bash_command)
        except:
            pass
            
        try:
            if hasattr(analysis_tools, 'analyze_code_activity'):
                tools.append(analysis_tools.analyze_code_activity)
        except:
            pass
            
        return create_react_agent(
            llm,
            tools=tools,
            prompt="You are a Coder agent. Your role is to write code, analyze data, and generate insights. Use available tools to execute code and analyze information.",
        )
    except Exception as e:
        logger.error(f"Error creating coder agent: {e}")
        return None


def create_reporter_agent():
    """Create reporter agent with basic LLM and no tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["reporter"])
        if not llm:
            logger.error("Failed to create LLM for reporter agent")
            return None
            
        return create_react_agent(
            llm,
            tools=[],
            prompt="You are a Reporter agent. Your role is to synthesize information and create comprehensive reports. Generate detailed reports based on the input.",
        )
    except Exception as e:
        logger.error(f"Error creating reporter agent: {e}")
        return None


def create_file_manager_agent():
    """Create file manager agent with file management tools."""
    try:
        llm = get_llm_by_type(AGENT_LLM_MAP["file_manager"])
        if not llm:
            logger.error("Failed to create LLM for file_manager agent")
            return None
        
        tools = []
        try:
            if hasattr(file_tools, 'save_report'):
                tools.append(file_tools.save_report)
        except:
            pass
            
        try:
            if hasattr(file_tools, 'write_file'):
                tools.append(file_tools.write_file)
        except:
            pass
            
        try:
            if hasattr(file_tools, 'read_file'):
                tools.append(file_tools.read_file)
        except:
            pass
            
        return create_react_agent(
            llm,
            tools=tools,
            prompt="You are a File Manager agent. Your role is to manage files, save reports, and organize output. Use available tools to handle file operations.",
        )
    except Exception as e:
        logger.error(f"Error creating file_manager agent: {e}")
        return None


# Create agent instances
coordinator_agent = create_coordinator_agent()
planner_agent = create_planner_agent()
researcher_agent = create_researcher_agent()
browser_agent = create_browser_agent()
coder_agent = create_coder_agent()
reporter_agent = create_reporter_agent()
file_manager_agent = create_file_manager_agent()

# Agent registry for easy access
AGENTS = {
    "coordinator": coordinator_agent,
    "planner": planner_agent,
    "researcher": researcher_agent,
    "browser": browser_agent,
    "coder": coder_agent,
    "reporter": reporter_agent,
    "file_manager": file_manager_agent,
}
