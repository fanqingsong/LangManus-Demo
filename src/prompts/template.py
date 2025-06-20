"""Prompt template engine for LangManus Demo."""

import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path


class PromptTemplate:
    """Template engine for loading and formatting prompts."""
    
    def __init__(self, prompts_dir: str = None):
        if prompts_dir is None:
            prompts_dir = os.path.join(os.path.dirname(__file__))
        self.prompts_dir = Path(prompts_dir)
        
    def load_prompt(self, agent_name: str, **kwargs) -> str:
        """Load and format a prompt template for an agent."""
        prompt_file = self.prompts_dir / f"{agent_name}.md"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
            
        with open(prompt_file, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # Add common variables
        context = {
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'team_members': ", ".join([
                "coordinator", "planner", "supervisor", 
                "researcher", "coder", "browser", "reporter"
            ]),
            **kwargs
        }
        
        # Simple template substitution
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            template = template.replace(placeholder, str(value))
            
        return template


# Global template instance
prompt_template = PromptTemplate() 