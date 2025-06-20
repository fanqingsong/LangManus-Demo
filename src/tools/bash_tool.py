"""Bash execution tools for LangManus Demo."""

import subprocess
import os
import tempfile
import shlex
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BashTool:
    """Safe bash command execution tool."""
    
    def __init__(self, working_dir: Optional[str] = None, timeout: int = 30):
        """Initialize bash tool.
        
        Args:
            working_dir: Working directory for commands
            timeout: Default timeout for commands
        """
        self.working_dir = working_dir or os.getcwd()
        self.timeout = timeout
        self.env = os.environ.copy()
    
    def execute(self, command: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Execute a bash command safely.
        
        Args:
            command: Bash command to execute
            timeout: Command timeout (uses default if None)
            
        Returns:
            Dict containing execution results
        """
        timeout = timeout or self.timeout
        
        try:
            # Validate command safety
            if not self._is_command_safe(command):
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": "Command blocked for security reasons",
                    "return_code": -1,
                    "command": command
                }
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_dir,
                env=self.env
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "command": command,
                "working_dir": self.working_dir
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Bash command timeout after {timeout}s: {command}")
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timeout after {timeout} seconds",
                "return_code": -1,
                "command": command
            }
        except Exception as e:
            logger.error(f"Error executing bash command: {e}")
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
                "command": command
            }
    
    def _is_command_safe(self, command: str) -> bool:
        """Check if a command is safe to execute.
        
        Args:
            command: Command to check
            
        Returns:
            True if command is safe
        """
        # List of dangerous commands to block
        dangerous_commands = [
            'rm -rf /',
            'sudo rm',
            'dd if=',
            'mkfs',
            'fdisk',
            'format',
            'del /f',
            'deltree',
            'shutdown',
            'reboot',
            'halt',
            'poweroff',
            'kill -9',
            'killall',
            'chmod 777',
            'chown root',
            'su -',
            'sudo su',
        ]
        
        command_lower = command.lower().strip()
        
        # Block obviously dangerous commands
        for dangerous in dangerous_commands:
            if dangerous in command_lower:
                logger.warning(f"Blocked dangerous command: {command}")
                return False
        
        return True
    
    def execute_script(self, script_content: str, script_name: str = "script.sh") -> Dict[str, Any]:
        """Execute a bash script from content.
        
        Args:
            script_content: Content of the bash script
            script_name: Name for the temporary script file
            
        Returns:
            Dict containing execution results
        """
        try:
            # Create temporary script file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                # Make script executable
                os.chmod(script_path, 0o755)
                
                # Execute script
                result = self.execute(f"bash {script_path}")
                result["script_content"] = script_content
                return result
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(script_path)
                except OSError:
                    pass
                    
        except Exception as e:
            logger.error(f"Error executing bash script: {e}")
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
                "script_content": script_content
            }


# Global bash tool instance
_bash_tool = BashTool()


def execute_bash_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """Execute a bash command using the global bash tool.
    
    Args:
        command: Bash command to execute
        timeout: Command timeout in seconds
        
    Returns:
        Dict containing execution results
    """
    return _bash_tool.execute(command, timeout)


def execute_bash_script(script_content: str, script_name: str = "script.sh") -> Dict[str, Any]:
    """Execute a bash script using the global bash tool.
    
    Args:
        script_content: Content of the bash script
        script_name: Name for the temporary script file
        
    Returns:
        Dict containing execution results
    """
    return _bash_tool.execute_script(script_content, script_name)
