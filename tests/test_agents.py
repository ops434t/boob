"""
Tests for AI Administrator agents
"""

import asyncio
import unittest
from ai_admin.core.orchestrator import Orchestrator
from ai_admin.core.agent import Agent, AgentResponse
from ai_admin.agents.system_monitor import SystemMonitorAgent
from ai_admin.agents.task_automation import TaskAutomationAgent
from ai_admin.agents.chat_interface import ChatInterfaceAgent


class TestAgentBase(unittest.TestCase):
    """Test base Agent class"""
    
    def test_agent_creation(self):
        """Test creating an agent"""
        
        class TestAgent(Agent):
            async def execute(self, task):
                return AgentResponse(
                    success=True,
                    data={"test": "data"},
                    message="Test message",
                    agent_name=self.name
                )
        
        agent = TestAgent("test", "Test agent")
        self.assertEqual(agent.name, "test")
        self.assertEqual(agent.description, "Test agent")
        self.assertTrue(agent.enabled)
    
    def test_agent_enable_disable(self):
        """Test enabling and disabling agents"""
        
        class TestAgent(Agent):
            async def execute(self, task):
                return AgentResponse(
                    success=True,
                    data={},
                    message="",
                    agent_name=self.name
                )
        
        agent = TestAgent("test", "Test")
        self.assertTrue(agent.enabled)
        
        agent.disable()
        self.assertFalse(agent.enabled)
        
        agent.enable()
        self.assertTrue(agent.enabled)


class TestOrchestrator(unittest.TestCase):
    """Test Orchestrator class"""
    
    def setUp(self):
        """Set up test orchestrator"""
        self.orchestrator = Orchestrator()
    
    def test_register_agent(self):
        """Test registering an agent"""
        agent = SystemMonitorAgent()
        self.orchestrator.register_agent(agent)
        
        self.assertIn("system_monitor", self.orchestrator.agents)
        self.assertEqual(
            self.orchestrator.get_agent("system_monitor"),
            agent
        )
    
    def test_unregister_agent(self):
        """Test unregistering an agent"""
        agent = SystemMonitorAgent()
        self.orchestrator.register_agent(agent)
        self.assertIn("system_monitor", self.orchestrator.agents)
        
        self.orchestrator.unregister_agent("system_monitor")
        self.assertNotIn("system_monitor", self.orchestrator.agents)
    
    def test_list_agents(self):
        """Test listing agents"""
        agent1 = SystemMonitorAgent()
        agent2 = TaskAutomationAgent()
        
        self.orchestrator.register_agent(agent1)
        self.orchestrator.register_agent(agent2)
        
        agents = self.orchestrator.list_agents()
        self.assertIn("system_monitor", agents)
        self.assertIn("task_automation", agents)
    
    def test_get_status(self):
        """Test getting orchestrator status"""
        agent = SystemMonitorAgent()
        self.orchestrator.register_agent(agent)
        
        status = self.orchestrator.get_status()
        self.assertEqual(status["total_agents"], 1)
        self.assertEqual(status["enabled_agents"], 1)
        self.assertIn("system_monitor", status["agents"])


class TestSystemMonitorAgent(unittest.TestCase):
    """Test SystemMonitorAgent"""
    
    def setUp(self):
        """Set up test agent"""
        self.agent = SystemMonitorAgent()
    
    def test_agent_creation(self):
        """Test agent is created correctly"""
        self.assertEqual(self.agent.name, "system_monitor")
        self.assertTrue(self.agent.enabled)
    
    def test_cpu_monitoring(self):
        """Test CPU monitoring"""
        async def run_test():
            response = await self.agent.execute({"action": "cpu"})
            self.assertTrue(response.success)
            self.assertIn("percent", response.data)
            self.assertIn("count", response.data)
            self.assertGreaterEqual(response.data["percent"], 0)
            self.assertLessEqual(response.data["percent"], 100)
        
        asyncio.run(run_test())
    
    def test_memory_monitoring(self):
        """Test memory monitoring"""
        async def run_test():
            response = await self.agent.execute({"action": "memory"})
            self.assertTrue(response.success)
            self.assertIn("virtual", response.data)
            self.assertIn("swap", response.data)
            self.assertGreaterEqual(response.data["virtual"]["percent"], 0)
        
        asyncio.run(run_test())
    
    def test_full_status(self):
        """Test full system status"""
        async def run_test():
            response = await self.agent.execute({"action": "full_status"})
            self.assertTrue(response.success)
            self.assertIn("platform", response.data)
            self.assertIn("cpu", response.data)
            self.assertIn("memory", response.data)
            self.assertIn("disk", response.data)
            self.assertIn("network", response.data)
        
        asyncio.run(run_test())
    
    def test_unknown_action(self):
        """Test unknown action handling"""
        async def run_test():
            response = await self.agent.execute({"action": "unknown"})
            self.assertFalse(response.success)
            self.assertIn("Unknown action", response.message)
        
        asyncio.run(run_test())


class TestTaskAutomationAgent(unittest.TestCase):
    """Test TaskAutomationAgent"""
    
    def setUp(self):
        """Set up test agent"""
        self.agent = TaskAutomationAgent()
    
    def test_agent_creation(self):
        """Test agent is created correctly"""
        self.assertEqual(self.agent.name, "task_automation")
        self.assertTrue(self.agent.enabled)
    
    def test_list_processes(self):
        """Test listing processes"""
        async def run_test():
            response = await self.agent.execute({"action": "list_processes"})
            self.assertTrue(response.success)
            self.assertIsInstance(response.data, list)
            self.assertGreater(len(response.data), 0)
            
            # Check process structure
            if len(response.data) > 0:
                proc = response.data[0]
                self.assertIn("pid", proc)
                self.assertIn("name", proc)
        
        asyncio.run(run_test())
    
    def test_list_directory(self):
        """Test listing directory"""
        async def run_test():
            import os
            response = await self.agent.execute({
                "action": "list_directory",
                "path": os.getcwd()
            })
            self.assertTrue(response.success)
            self.assertIn("files", response.data)
            self.assertIn("directories", response.data)
            self.assertIn("path", response.data)
        
        asyncio.run(run_test())
    
    def test_get_environment(self):
        """Test getting environment variables"""
        async def run_test():
            response = await self.agent.execute({"action": "get_environment"})
            self.assertTrue(response.success)
            self.assertIsInstance(response.data, dict)
        
        asyncio.run(run_test())


class TestChatInterfaceAgent(unittest.TestCase):
    """Test ChatInterfaceAgent"""
    
    def setUp(self):
        """Set up test agent"""
        self.agent = ChatInterfaceAgent()
    
    def test_agent_creation(self):
        """Test agent is created correctly"""
        self.assertEqual(self.agent.name, "chat_interface")
        self.assertTrue(self.agent.enabled)
        self.assertEqual(len(self.agent.conversation_history), 0)
    
    def test_chat(self):
        """Test chat functionality"""
        async def run_test():
            response = await self.agent.execute({
                "action": "chat",
                "message": "Hello"
            })
            self.assertTrue(response.success)
            self.assertIn("response", response.data)
            self.assertIn("user_message", response.data)
            self.assertEqual(response.data["user_message"], "Hello")
            
            # Check history was updated
            self.assertEqual(len(self.agent.conversation_history), 2)
        
        asyncio.run(run_test())
    
    def test_get_history(self):
        """Test getting chat history"""
        async def run_test():
            # Send a message first
            await self.agent.execute({
                "action": "chat",
                "message": "Test"
            })
            
            # Get history
            response = await self.agent.execute({"action": "history"})
            self.assertTrue(response.success)
            self.assertIn("history", response.data)
            self.assertGreater(len(response.data["history"]), 0)
        
        asyncio.run(run_test())
    
    def test_clear_history(self):
        """Test clearing chat history"""
        async def run_test():
            # Send a message
            await self.agent.execute({
                "action": "chat",
                "message": "Test"
            })
            self.assertGreater(len(self.agent.conversation_history), 0)
            
            # Clear history
            response = await self.agent.execute({"action": "clear"})
            self.assertTrue(response.success)
            self.assertEqual(len(self.agent.conversation_history), 0)
        
        asyncio.run(run_test())


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_system(self):
        """Test complete system with all agents"""
        async def run_test():
            orchestrator = Orchestrator()
            
            # Register all agents
            orchestrator.register_agent(SystemMonitorAgent())
            orchestrator.register_agent(TaskAutomationAgent())
            orchestrator.register_agent(ChatInterfaceAgent())
            
            # Test each agent
            cpu_response = await orchestrator.delegate_task(
                "system_monitor",
                {"action": "cpu"}
            )
            self.assertTrue(cpu_response.success)
            
            proc_response = await orchestrator.delegate_task(
                "task_automation",
                {"action": "list_processes"}
            )
            self.assertTrue(proc_response.success)
            
            chat_response = await orchestrator.delegate_task(
                "chat_interface",
                {"action": "chat", "message": "Hello"}
            )
            self.assertTrue(chat_response.success)
        
        asyncio.run(run_test())
    
    def test_disabled_agent(self):
        """Test delegating to disabled agent"""
        async def run_test():
            orchestrator = Orchestrator()
            agent = SystemMonitorAgent()
            agent.disable()
            orchestrator.register_agent(agent)
            
            response = await orchestrator.delegate_task(
                "system_monitor",
                {"action": "cpu"}
            )
            self.assertFalse(response.success)
            self.assertIn("disabled", response.message)
        
        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
