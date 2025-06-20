"""File management tools for LangManus Demo."""

import os
import json
import csv
from pathlib import Path
from typing import Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)


def read_file(file_path: str) -> Dict[str, Any]:
    """Read content from a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Dict containing file content and metadata
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {file_path}",
                "content": None
            }
        
        # Read based on file extension
        if path.suffix.lower() == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)
        elif path.suffix.lower() == '.csv':
            content = []
            with open(path, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                content = list(csv_reader)
        else:
            # Text files (including .md, .txt, .py, etc.)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        return {
            "success": True,
            "content": content,
            "file_path": str(path),
            "file_size": path.stat().st_size,
            "file_type": path.suffix.lower()
        }
        
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return {
            "success": False,
            "error": str(e),
            "content": None
        }


def write_file(file_path: str, content: Union[str, dict, list], create_dirs: bool = True) -> Dict[str, Any]:
    """Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        create_dirs: Whether to create parent directories
        
    Returns:
        Dict containing operation results
    """
    try:
        path = Path(file_path)
        
        # Create parent directories if needed
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write based on file extension and content type
        if path.suffix.lower() == '.json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        elif path.suffix.lower() == '.csv' and isinstance(content, list):
            with open(path, 'w', encoding='utf-8', newline='') as f:
                if content and isinstance(content[0], dict):
                    fieldnames = content[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(content)
                else:
                    writer = csv.writer(f)
                    writer.writerows(content)
        else:
            # Text files
            content_str = content if isinstance(content, str) else str(content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content_str)
        
        return {
            "success": True,
            "file_path": str(path),
            "file_size": path.stat().st_size,
            "message": f"Successfully wrote to {file_path}"
        }
        
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def save_report(report_content: str, filename: str = "report.md", output_dir: str = "output") -> Dict[str, Any]:
    """Save a report to a markdown file.
    
    Args:
        report_content: Content of the report
        filename: Name of the report file
        output_dir: Output directory
        
    Returns:
        Dict containing operation results
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return {
            "success": True,
            "file_path": str(file_path),
            "message": f"Report saved to {file_path}"
        }
        
    except Exception as e:
        logger.error(f"Error saving report: {e}")
        return {
            "success": False,
            "error": str(e)
        }
