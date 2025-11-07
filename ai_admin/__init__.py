"""
AI Administrator - An AI-powered PC administrator assistant using agents
"""

from .core.agent import Agent, AgentResponse
from .core.orchestrator import Orchestrator
from .agents.system_monitor import SystemMonitorAgent
from .agents.task_automation import TaskAutomationAgent
from .agents.chat_interface import ChatInterfaceAgent

__version__ = "0.1.0"
__all__ = [
    "Agent",
    "AgentResponse",
    "Orchestrator",
    "SystemMonitorAgent",
    "TaskAutomationAgent",
    "ChatInterfaceAgent",
]
