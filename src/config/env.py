"""Environment configuration for LangManus Demo."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMConfig:
    """LLM Configuration class."""
    
    def __init__(self, model: str, api_key: str, base_url: Optional[str] = None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url


# Reasoning LLM Configuration (for complex reasoning tasks)
REASONING_LLM = LLMConfig(
    model=os.getenv("REASONING_MODEL", "gpt-4o"),
    api_key=os.getenv("REASONING_API_KEY", ""),
    base_url=os.getenv("REASONING_BASE_URL", "https://api.openai.com/v1")
)

# Basic LLM Configuration (for simpler tasks)
BASIC_LLM = LLMConfig(
    model=os.getenv("BASIC_MODEL", "gpt-4o-mini"),
    api_key=os.getenv("BASIC_API_KEY", ""),
    base_url=os.getenv("BASIC_BASE_URL", "https://api.openai.com/v1")
)

# Vision-Language LLM Configuration (for tasks involving images)
VL_LLM = LLMConfig(
    model=os.getenv("VL_MODEL", "gpt-4o"),
    api_key=os.getenv("VL_API_KEY", ""),
    base_url=os.getenv("VL_BASE_URL", "https://api.openai.com/v1")
)

# Tool API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Browser Configuration
CHROME_INSTANCE_PATH = os.getenv("CHROME_INSTANCE_PATH", "") 