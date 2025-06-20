"""Agent configuration for LangManus Demo."""

# Team member configuration
TEAM_MEMBERS = [
    "coordinator",
    "planner", 
    "supervisor",
    "researcher",
    "coder",
    "browser",
    "reporter",
    "file_manager"
]

# Agent LLM mapping - defines which LLM type each agent uses
AGENT_LLM_MAP = {
    "coordinator": "basic",
    "planner": "reasoning", 
    "supervisor": "basic",
    "researcher": "basic",
    "coder": "basic",
    "browser": "basic",
    "reporter": "basic",
    "file_manager": "basic"
}

# Agent timeouts (in seconds)
AGENT_TIMEOUT = 300

# Maximum iterations for agent loops
MAX_ITERATIONS = 10 