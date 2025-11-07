"""Utility functions for AI Administrator"""

import json
from typing import Any, Dict, List
from datetime import datetime


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable format
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_percentage(value: float, total: float) -> str:
    """
    Format a value as percentage of total
    
    Args:
        value: Current value
        total: Total value
        
    Returns:
        Formatted percentage string
    """
    if total == 0:
        return "0.00%"
    return f"{(value / total * 100):.2f}%"


def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()


def safe_json_serialize(obj: Any) -> str:
    """
    Safely serialize object to JSON
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON string
    """
    def default_handler(o):
        if hasattr(o, '__dict__'):
            return o.__dict__
        return str(o)
    
    return json.dumps(obj, default=default_handler, indent=2)


def validate_path(path: str, allowed_paths: List[str] = None) -> bool:
    """
    Validate if a path is safe to access
    
    Args:
        path: Path to validate
        allowed_paths: List of allowed path prefixes
        
    Returns:
        True if path is safe, False otherwise
    """
    import os
    
    # Check if path exists
    if not os.path.exists(path):
        return False
    
    # Resolve symlinks and normalize the path to prevent traversal attacks
    real_path = os.path.realpath(path)
    
    # If allowed_paths specified, check if path is within allowed directories
    if allowed_paths:
        for allowed in allowed_paths:
            allowed_real = os.path.realpath(allowed)
            try:
                # Check if real_path is within allowed_real using commonpath
                common = os.path.commonpath([real_path, allowed_real])
                if common == allowed_real:
                    return True
            except (ValueError, TypeError):
                # Different drives on Windows or other path issues
                continue
        return False
    
    return True


def create_progress_bar(percentage: float, width: int = 20) -> str:
    """
    Create a text-based progress bar
    
    Args:
        percentage: Percentage (0-100)
        width: Width of the progress bar
        
    Returns:
        Progress bar string
    """
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percentage:.1f}%"


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate a string to max length
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_task_command(command: str) -> Dict[str, Any]:
    """
    Parse a natural language command into a task dictionary
    
    Args:
        command: Natural language command
        
    Returns:
        Task dictionary
    """
    command_lower = command.lower()
    
    # Simple command parsing
    if any(word in command_lower for word in ['monitor', 'check', 'status', 'system']):
        return {"action": "full_status"}
    elif 'cpu' in command_lower:
        return {"action": "cpu"}
    elif any(word in command_lower for word in ['memory', 'ram']):
        return {"action": "memory"}
    elif 'disk' in command_lower:
        return {"action": "disk"}
    elif any(word in command_lower for word in ['network', 'net']):
        return {"action": "network"}
    elif any(word in command_lower for word in ['process', 'processes']):
        return {"action": "list_processes"}
    elif any(word in command_lower for word in ['directory', 'folder', 'ls', 'dir']):
        return {"action": "list_directory"}
    else:
        return {"action": "chat", "message": command}
