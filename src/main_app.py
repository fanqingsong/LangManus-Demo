"""Main LangManus Demo application."""

import logging
from typing import Dict, Any
from src.core.workflow import create_workflow, WorkflowState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LangManusAgent:
    """LangManus-powered GitHub repository analyzer."""
    
    def __init__(self, task: str = None):
        """Initialize the agent with a task.
        
        Args:
            task: Task description for the agent
        """
        self.task = task or "Find a popular open-source project updated recently and summarize its new features with examples and charts."
        self.workflow = create_workflow()
        
    def run(self) -> Dict[str, Any]:
        """Run the complete workflow.
        
        Returns:
            Dict containing the final state
        """
        try:
            # Initialize workflow state
            initial_state: WorkflowState = {
                "messages": [],
                "task": self.task,
                "current_step": "start",
                "repo_url": "",
                "repo_data": {},
                "analysis": [],
                "chart_paths": [],
                "report": "",
                "error": ""
            }
            
            logger.info(f"Starting workflow with task: {self.task}")
            
            # Execute workflow
            final_state = self.workflow.invoke(initial_state)
            
            if final_state.get("error"):
                logger.error(f"Workflow failed: {final_state['error']}")
            else:
                logger.info("Workflow completed successfully")
                
            return final_state
            
        except Exception as e:
            logger.error(f"Error running workflow: {e}")
            return {
                "error": str(e),
                "report": f"Failed to complete analysis: {str(e)}",
                "chart_paths": []
            }
    
    def run_and_return(self) -> tuple[str, list[str]]:
        """Run workflow and return report and chart paths.
        
        Returns:
            Tuple of (report, chart_paths)
        """
        result = self.run()
        return result.get("report", ""), result.get("chart_paths", [])
    
    def stream_run(self):
        """Run workflow with streaming updates."""
        try:
            # Initialize workflow state
            initial_state: WorkflowState = {
                "messages": [],
                "task": self.task,
                "current_step": "start",
                "repo_url": "",
                "repo_data": {},
                "analysis": [],
                "chart_paths": [],
                "report": "",
                "error": ""
            }
            
            # Stream workflow execution
            for state in self.workflow.stream(initial_state):
                yield state
                
        except Exception as e:
            logger.error(f"Error in streaming workflow: {e}")
            yield {"error": str(e)}


def main():
    """Main entry point."""
    agent = LangManusAgent()
    result = agent.run()
    
    if result.get("error"):
        print(f"❌ Error: {result['error']}")
    else:
        print("✅ Analysis completed!")
        print("\n" + "="*60)
        print(result.get("report", "No report generated"))
        print("="*60)
        
        chart_paths = result.get("chart_paths", [])
        if chart_paths:
            print(f"\n📊 Generated {len(chart_paths)} charts:")
            for path in chart_paths:
                print(f"  - {path}")


if __name__ == "__main__":
    main() 