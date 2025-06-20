"""Tool configuration for LangManus Demo.

This module configures tools that can be attached to agents.
Tools are modular and can be easily added or removed based on business requirements.
"""

# Core search tools configuration
TAVILY_MAX_RESULTS = 5

# GitHub tools configuration (Business-specific tools)
# These tools provide GitHub-specific functionality and can be attached to agents as needed
GITHUB_MAX_COMMITS = 20
GITHUB_TOKEN = None  # Set via environment variable

# Analysis tools configuration
COMMIT_CATEGORIES = {
    'feature': ['feat', 'feature', 'add', 'implement', 'create'],
    'fix': ['fix', 'bug', 'patch', 'resolve', 'correct'],
    'docs': ['docs', 'doc', 'documentation', 'readme'],
    'refactor': ['refactor', 'refact', 'restructure', 'optimize'],
    'test': ['test', 'tests', 'testing', 'spec'],
    'style': ['style', 'format', 'lint', 'prettier'],
    'chore': ['chore', 'update', 'upgrade', 'deps', 'dependencies'],
    'ci': ['ci', 'build', 'deploy', 'pipeline']
}

# Chart generation settings
CHART_DPI = 150
CHART_FIGSIZE = (12, 8)

# File output settings
OUTPUT_DIR = "output"
CHARTS_DIR = "charts"
CHART_OUTPUT_DIR = OUTPUT_DIR  # Alias for backward compatibility

# Chart Configuration
CHART_FIGURE_SIZE = (10, 6)
COMMIT_CHART_NAME = "commit_chart.png"
CATEGORY_CHART_NAME = "category_chart.png"
TOPICS_CHART_NAME = "topics_chart.png" 