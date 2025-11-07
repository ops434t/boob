"""
Core Agent base class for the AI Administrator system
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AgentResponse:
    """Response from an agent"""
    success: bool
    data: Any
    message: str
    agent_name: str
    

class Agent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True
        
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        """
        Execute a task and return a response
        
        Args:
            task: Dictionary containing task information
            
        Returns:
            AgentResponse object with results
        """
        pass
    
    def enable(self):
        """Enable this agent"""
        self.enabled = True
        
    def disable(self):
        """Disable this agent"""
        self.enabled = False
        
    def __repr__(self):
        return f"<Agent {self.name}: {self.description}>"
