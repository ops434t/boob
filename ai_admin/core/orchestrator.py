"""
Orchestrator - Coordinates multiple agents to accomplish complex tasks
"""

from typing import List, Dict, Any, Optional
import asyncio
from .agent import Agent, AgentResponse


class Orchestrator:
    """Manages and coordinates multiple agents"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        
    def register_agent(self, agent: Agent):
        """
        Register a new agent with the orchestrator
        
        Args:
            agent: Agent instance to register
        """
        self.agents[agent.name] = agent
        print(f"✓ Registered agent: {agent.name}")
        
    def unregister_agent(self, agent_name: str):
        """
        Unregister an agent
        
        Args:
            agent_name: Name of the agent to unregister
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            print(f"✓ Unregistered agent: {agent_name}")
            
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(agent_name)
        
    def list_agents(self) -> List[str]:
        """Get list of all registered agents"""
        return list(self.agents.keys())
        
    async def delegate_task(self, agent_name: str, task: Dict[str, Any]) -> AgentResponse:
        """
        Delegate a task to a specific agent
        
        Args:
            agent_name: Name of the agent to execute the task
            task: Task dictionary
            
        Returns:
            AgentResponse from the agent
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return AgentResponse(
                success=False,
                data=None,
                message=f"Agent '{agent_name}' not found",
                agent_name="orchestrator"
            )
            
        if not agent.enabled:
            return AgentResponse(
                success=False,
                data=None,
                message=f"Agent '{agent_name}' is disabled",
                agent_name="orchestrator"
            )
            
        return await agent.execute(task)
        
    async def broadcast_task(self, task: Dict[str, Any]) -> List[AgentResponse]:
        """
        Broadcast a task to all enabled agents
        
        Args:
            task: Task dictionary
            
        Returns:
            List of AgentResponse objects
        """
        tasks = [
            agent.execute(task)
            for agent in self.agents.values()
            if agent.enabled
        ]
        
        if not tasks:
            return []
            
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        results = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                results.append(AgentResponse(
                    success=False,
                    data=None,
                    message=f"Error: {str(response)}",
                    agent_name="orchestrator"
                ))
            else:
                results.append(response)
                
        return results
        
    def get_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "total_agents": len(self.agents),
            "enabled_agents": sum(1 for a in self.agents.values() if a.enabled),
            "agents": {
                name: {
                    "enabled": agent.enabled,
                    "description": agent.description
                }
                for name, agent in self.agents.items()
            }
        }
