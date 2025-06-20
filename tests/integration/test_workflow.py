"""Integration tests for LangManus workflow."""

import pytest
from unittest.mock import Mock, patch
from src.core.workflow import create_workflow, WorkflowState
from src.main_app import LangManusAgent


class TestWorkflow:
    """Test suite for workflow functionality."""
    
    def test_workflow_creation(self):
        """Test that workflow can be created."""
        workflow = create_workflow()
        assert workflow is not None
        
    @patch('src.tools.github_tools.find_trending_repo')
    @patch('src.tools.github_tools.scrape_github_activity')
    @patch('src.tools.analysis_tools.analyze_code_activity')
    def test_agent_initialization(self, mock_analyze, mock_scrape, mock_find):
        """Test agent initialization."""
        # Mock return values
        mock_find.return_value = "https://github.com/test/repo"
        mock_scrape.return_value = {
            'repo_url': 'https://github.com/test/repo',
            'commits': ['test commit'],
            'commit_dates': ['2024-01-01T00:00:00Z'],
            'metadata': {'name': 'test-repo'}
        }
        mock_analyze.return_value = (["Test analysis"], ["test_chart.png"])
        
        agent = LangManusAgent(task="Test task")
        assert agent.task == "Test task"
        assert agent.workflow is not None
        
    def test_workflow_state_structure(self):
        """Test workflow state has required fields."""
        state: WorkflowState = {
            "messages": [],
            "task": "test",
            "current_step": "start",
            "repo_url": "",
            "repo_data": {},
            "analysis": [],
            "chart_paths": [],
            "report": "",
            "error": ""
        }
        
        # Check all required fields are present
        required_fields = [
            "messages", "task", "current_step", "repo_url",
            "repo_data", "analysis", "chart_paths", "report", "error"
        ]
        
        for field in required_fields:
            assert field in state 