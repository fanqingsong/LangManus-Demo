"""Python execution tools for LangManus Demo."""

import subprocess
import sys
import tempfile
import os
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


def execute_python_code(code: str, timeout: int = 30) -> Dict[str, Any]:
    """Execute Python code in a safe environment.
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Dict containing execution results
    """
    try:
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute the code using subprocess
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "executed_code": code
            }
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except OSError:
                pass
                
    except subprocess.TimeoutExpired:
        logger.error(f"Python code execution timeout after {timeout}s")
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timeout after {timeout} seconds",
            "return_code": -1,
            "executed_code": code
        }
    except Exception as e:
        logger.error(f"Error executing Python code: {e}")
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "return_code": -1,
            "executed_code": code
        }


def install_package(package: str) -> Dict[str, Any]:
    """Install a Python package using pip.
    
    Args:
        package: Package name to install
        
    Returns:
        Dict containing installation results
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "package": package
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Package installation timeout for {package}",
            "package": package
        }
    except Exception as e:
        logger.error(f"Error installing package {package}: {e}")
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "package": package
        }


def run_shell_command(command: str, timeout: int = 30) -> Dict[str, Any]:
    """Execute a shell command safely.
    
    Args:
        command: Shell command to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Dict containing execution results
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": command
        }
        
    except subprocess.TimeoutExpired:
        logger.error(f"Shell command timeout after {timeout}s: {command}")
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timeout after {timeout} seconds",
            "return_code": -1,
            "command": command
        }
    except Exception as e:
        logger.error(f"Error executing shell command: {e}")
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "return_code": -1,
            "command": command
        }


def check_python_environment() -> Dict[str, Any]:
    """Check Python environment information.
    
    Returns:
        Dict containing environment information
    """
    try:
        import platform
        
        env_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
            "path": sys.path[:5],  # First 5 paths to avoid too much data
            "working_directory": os.getcwd()
        }
        
        return {
            "success": True,
            "environment": env_info
        }
        
    except Exception as e:
        logger.error(f"Error checking Python environment: {e}")
        return {
            "success": False,
            "error": str(e)
        }


class PythonREPL:
    """Simple Python REPL for interactive code execution."""
    
    def __init__(self):
        self.globals = {}
        self.locals = {}
    
    def execute(self, code: str) -> Dict[str, Any]:
        """Execute code in the REPL environment.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dict containing execution results
        """
        try:
            # Try to compile and execute the code
            compiled_code = compile(code, '<repl>', 'exec')
            
            # Capture stdout
            import io
            import contextlib
            
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                exec(compiled_code, self.globals, self.locals)
            
            stdout = stdout_capture.getvalue()
            stderr = stderr_capture.getvalue()
            
            return {
                "success": True,
                "stdout": stdout,
                "stderr": stderr,
                "executed_code": code
            }
            
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "executed_code": code
            }
    
    def reset(self):
        """Reset the REPL environment."""
        self.globals.clear()
        self.locals.clear()


# Global REPL instance for maintaining state
_repl = PythonREPL()


def execute_repl_code(code: str) -> Dict[str, Any]:
    """Execute code in a persistent REPL environment.
    
    Args:
        code: Python code to execute
        
    Returns:
        Dict containing execution results
    """
    return _repl.execute(code)


def reset_repl():
    """Reset the REPL environment."""
    _repl.reset()
    return {"success": True, "message": "REPL environment reset"} 