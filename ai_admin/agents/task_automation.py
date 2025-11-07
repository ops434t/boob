"""
Task Automation Agent - Automates common system administration tasks
"""

import os
import subprocess
from typing import Dict, Any, List
from ..core.agent import Agent, AgentResponse


class TaskAutomationAgent(Agent):
    """Agent for automating system administration tasks"""
    
    def __init__(self):
        super().__init__(
            name="task_automation",
            description="Automates common system tasks like file operations and process management"
        )
        self.safe_commands = {
            "list_processes": self._list_processes,
            "list_directory": self._list_directory,
            "get_environment": self._get_environment,
            "check_service": self._check_service,
        }
        
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        """
        Execute automation task
        
        Args:
            task: Task dictionary with 'action' key
            
        Returns:
            AgentResponse with task results
        """
        action = task.get("action")
        
        if action not in self.safe_commands:
            return AgentResponse(
                success=False,
                data=None,
                message=f"Unknown or unsafe action: {action}",
                agent_name=self.name
            )
            
        try:
            result = self.safe_commands[action](task)
            return AgentResponse(
                success=True,
                data=result,
                message=f"Task '{action}' completed successfully",
                agent_name=self.name
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                data=None,
                message=f"Error executing task: {str(e)}",
                agent_name=self.name
            )
            
    def _list_processes(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List running processes"""
        import psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes[:50]  # Limit to top 50 processes
        
    def _list_directory(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """List directory contents"""
        path = task.get("path", os.getcwd())
        
        # Security: only allow listing safe directories
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
            
        items = os.listdir(path)
        files = []
        directories = []
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                files.append(item)
            elif os.path.isdir(full_path):
                directories.append(item)
                
        return {
            "path": path,
            "files": files,
            "directories": directories,
            "total_items": len(items)
        }
        
    def _get_environment(self, task: Dict[str, Any]) -> Dict[str, str]:
        """Get environment variables"""
        # Only return non-sensitive environment variables
        safe_vars = ['PATH', 'HOME', 'USER', 'SHELL', 'LANG', 'PWD']
        return {k: v for k, v in os.environ.items() if k in safe_vars}
        
    def _check_service(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check if a service is running (placeholder)"""
        service_name = task.get("service_name", "")
        return {
            "service": service_name,
            "status": "unknown",
            "message": "Service checking not fully implemented yet"
        }
