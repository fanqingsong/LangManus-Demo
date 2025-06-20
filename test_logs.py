#!/usr/bin/env python3
"""Test script to verify logging functionality."""

import logging
from src.core.workflow import coordinator_node, WorkflowState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def test_coordinator_logs():
    """Test coordinator node logging."""
    print("🧪 Testing Coordinator Node Logging...")
    
    # Create test state
    state = WorkflowState(
        messages=[],
        task="Analyze a trending GitHub repository",
        current_step="coordinator",
        repo_url="",
        repo_data={},
        analysis=[],
        chart_paths=[],
        report="",
        error=""
    )
    
    try:
        # This will fail due to missing LLM, but we can see the logs
        result = coordinator_node(state)
        print("✅ Coordinator logs test completed")
        return result
    except Exception as e:
        print(f"❌ Expected error (no LLM configured): {e}")
        return state

if __name__ == "__main__":
    test_coordinator_logs()
