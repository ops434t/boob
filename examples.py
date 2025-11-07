"""
Example usage of AI Administrator as a library
"""

import asyncio
from ai_admin.core.orchestrator import Orchestrator
from ai_admin.agents.system_monitor import SystemMonitorAgent
from ai_admin.agents.task_automation import TaskAutomationAgent
from ai_admin.agents.chat_interface import ChatInterfaceAgent


async def example_system_monitoring():
    """Example: Monitor system resources"""
    print("=" * 60)
    print("Example 1: System Monitoring")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    orchestrator.register_agent(SystemMonitorAgent())
    
    # Get CPU information
    print("\n1. Getting CPU info...")
    response = await orchestrator.delegate_task("system_monitor", {"action": "cpu"})
    if response.success:
        print(f"CPU Usage: {response.data['percent']}%")
        print(f"CPU Cores: {response.data['count']}")
    
    # Get memory information
    print("\n2. Getting memory info...")
    response = await orchestrator.delegate_task("system_monitor", {"action": "memory"})
    if response.success:
        mem = response.data['virtual']
        print(f"Memory Usage: {mem['percent']}%")
        print(f"Available: {mem['available'] / (1024**3):.2f} GB")
    
    # Get full system status
    print("\n3. Getting full system status...")
    response = await orchestrator.delegate_task("system_monitor", {"action": "full_status"})
    if response.success:
        print(f"Platform: {response.data['platform']['system']}")
        print(f"Processor: {response.data['platform']['processor']}")


async def example_task_automation():
    """Example: Automate tasks"""
    print("\n" + "=" * 60)
    print("Example 2: Task Automation")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    orchestrator.register_agent(TaskAutomationAgent())
    
    # List processes
    print("\n1. Listing processes...")
    response = await orchestrator.delegate_task("task_automation", {"action": "list_processes"})
    if response.success:
        print(f"Found {len(response.data)} processes")
        print("Top 5 processes:")
        for proc in response.data[:5]:
            print(f"  - {proc['name']} (PID: {proc['pid']})")
    
    # List directory
    print("\n2. Listing current directory...")
    import os
    response = await orchestrator.delegate_task("task_automation", {
        "action": "list_directory",
        "path": os.getcwd()
    })
    if response.success:
        print(f"Path: {response.data['path']}")
        print(f"Directories: {len(response.data['directories'])}")
        print(f"Files: {len(response.data['files'])}")


async def example_chat_interface():
    """Example: Chat with the assistant"""
    print("\n" + "=" * 60)
    print("Example 3: Chat Interface")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    orchestrator.register_agent(ChatInterfaceAgent())
    
    # Chat examples
    messages = [
        "Hello!",
        "What can you do?",
        "Tell me about system monitoring",
        "Thanks for your help"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = await orchestrator.delegate_task("chat_interface", {
            "action": "chat",
            "message": msg
        })
        if response.success:
            print(f"Assistant: {response.data['response']}")


async def example_multi_agent():
    """Example: Multiple agents working together"""
    print("\n" + "=" * 60)
    print("Example 4: Multi-Agent Coordination")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    
    # Register all agents
    orchestrator.register_agent(SystemMonitorAgent())
    orchestrator.register_agent(TaskAutomationAgent())
    orchestrator.register_agent(ChatInterfaceAgent())
    
    # Check orchestrator status
    print("\n1. Orchestrator Status:")
    status = orchestrator.get_status()
    print(f"Total Agents: {status['total_agents']}")
    print(f"Enabled Agents: {status['enabled_agents']}")
    print("\nRegistered Agents:")
    for name, info in status['agents'].items():
        print(f"  - {name}: {info['description']}")
    
    # Execute tasks across different agents
    print("\n2. Executing tasks across agents...")
    
    # Monitor system
    sys_response = await orchestrator.delegate_task("system_monitor", {"action": "cpu"})
    print(f"System CPU: {sys_response.data['percent']}%")
    
    # Get process count
    task_response = await orchestrator.delegate_task("task_automation", {"action": "list_processes"})
    print(f"Running Processes: {len(task_response.data)}")
    
    # Chat about it
    chat_response = await orchestrator.delegate_task("chat_interface", {
        "action": "chat",
        "message": "Tell me about the system status"
    })
    print(f"Assistant says: {chat_response.data['response']}")


async def example_agent_control():
    """Example: Enable/disable agents"""
    print("\n" + "=" * 60)
    print("Example 5: Agent Control")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    agent = SystemMonitorAgent()
    orchestrator.register_agent(agent)
    
    # Check initial status
    print(f"\n1. Agent enabled: {agent.enabled}")
    
    # Disable agent
    print("\n2. Disabling agent...")
    agent.disable()
    response = await orchestrator.delegate_task("system_monitor", {"action": "cpu"})
    print(f"Response success: {response.success}")
    print(f"Message: {response.message}")
    
    # Re-enable agent
    print("\n3. Re-enabling agent...")
    agent.enable()
    response = await orchestrator.delegate_task("system_monitor", {"action": "cpu"})
    print(f"Response success: {response.success}")
    print(f"CPU Usage: {response.data['percent']}%")


async def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("AI Administrator - Library Usage Examples")
    print("=" * 60)
    
    await example_system_monitoring()
    await example_task_automation()
    await example_chat_interface()
    await example_multi_agent()
    await example_agent_control()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
