"""
Demo script showing AI Administrator in action
Run this to see a quick demonstration of capabilities
"""

import asyncio
import time
from colorama import init, Fore, Style
from ai_admin.core.orchestrator import Orchestrator
from ai_admin.agents.system_monitor import SystemMonitorAgent
from ai_admin.agents.task_automation import TaskAutomationAgent
from ai_admin.agents.chat_interface import ChatInterfaceAgent

# Initialize colorama
init(autoreset=True)


def print_section(title):
    """Print a section header"""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.YELLOW}{title:^70}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def print_success(message):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_info(key, value):
    """Print info line"""
    print(f"{Fore.CYAN}{key}:{Style.RESET_ALL} {value}")


async def demo_introduction():
    """Show introduction"""
    print_section("Welcome to AI Administrator Demo!")
    
    print(f"{Fore.MAGENTA}This demo will showcase the capabilities of your AI-powered")
    print(f"PC administrator assistant built with intelligent agents.{Style.RESET_ALL}\n")
    
    await asyncio.sleep(1)


async def demo_agent_setup():
    """Demonstrate agent setup"""
    print_section("Step 1: Setting Up Agents")
    
    orchestrator = Orchestrator()
    
    print("Initializing AI Administrator agents...\n")
    await asyncio.sleep(0.5)
    
    orchestrator.register_agent(SystemMonitorAgent())
    await asyncio.sleep(0.3)
    
    orchestrator.register_agent(TaskAutomationAgent())
    await asyncio.sleep(0.3)
    
    orchestrator.register_agent(ChatInterfaceAgent())
    await asyncio.sleep(0.3)
    
    print()
    print_success("All agents initialized successfully!")
    
    status = orchestrator.get_status()
    print_info("Total Agents", status["total_agents"])
    print_info("Active Agents", status["enabled_agents"])
    
    return orchestrator


async def demo_system_monitoring(orchestrator):
    """Demonstrate system monitoring"""
    print_section("Step 2: System Monitoring")
    
    print("Requesting system status from System Monitor Agent...\n")
    await asyncio.sleep(0.5)
    
    response = await orchestrator.delegate_task("system_monitor", {"action": "full_status"})
    
    if response.success:
        data = response.data
        
        print_success("System information retrieved!")
        print()
        
        # Platform info
        print(f"{Fore.YELLOW}Platform Information:{Style.RESET_ALL}")
        print_info("  OS", f"{data['platform']['system']} {data['platform']['release']}")
        print_info("  Architecture", data['platform']['machine'])
        print()
        
        # CPU info
        print(f"{Fore.YELLOW}CPU Status:{Style.RESET_ALL}")
        print_info("  Usage", f"{data['cpu']['percent']}%")
        print_info("  Total Cores", data['cpu']['count'])
        print_info("  Physical Cores", data['cpu']['count_physical'])
        print()
        
        # Memory info
        print(f"{Fore.YELLOW}Memory Status:{Style.RESET_ALL}")
        mem = data['memory']['virtual']
        print_info("  Usage", f"{mem['percent']}%")
        print_info("  Total", f"{mem['total'] / (1024**3):.2f} GB")
        print_info("  Available", f"{mem['available'] / (1024**3):.2f} GB")
        print_info("  Used", f"{mem['used'] / (1024**3):.2f} GB")
        print()
        
        # Disk info
        print(f"{Fore.YELLOW}Disk Status:{Style.RESET_ALL}")
        for i, part in enumerate(data['disk']['partitions'][:2], 1):
            print(f"  Partition {i}: {part['mountpoint']}")
            print_info("    Usage", f"{part['percent']}%")
            print_info("    Free Space", f"{part['free'] / (1024**3):.2f} GB")


async def demo_task_automation(orchestrator):
    """Demonstrate task automation"""
    print_section("Step 3: Task Automation")
    
    print("Requesting process list from Task Automation Agent...\n")
    await asyncio.sleep(0.5)
    
    response = await orchestrator.delegate_task("task_automation", {"action": "list_processes"})
    
    if response.success:
        processes = response.data[:10]
        print_success(f"Found {len(response.data)} running processes!")
        print()
        
        print(f"{Fore.YELLOW}Top 10 Processes:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'PID':<10} {'Name':<35} {'CPU%':<10} {'Memory%':<10}{Style.RESET_ALL}")
        print("-" * 65)
        
        for proc in processes:
            print(f"{proc['pid']:<10} {proc['name'][:33]:<35} "
                  f"{proc['cpu_percent']:<10.1f} {proc['memory_percent']:<10.2f}")


async def demo_chat_interface(orchestrator):
    """Demonstrate chat interface"""
    print_section("Step 4: Chat Interface")
    
    print("Interacting with Chat Interface Agent...\n")
    await asyncio.sleep(0.5)
    
    conversations = [
        ("Hello!", "Greeting the assistant"),
        ("What can you do?", "Asking about capabilities"),
        ("Tell me about system monitoring", "Asking for help"),
    ]
    
    for message, description in conversations:
        print(f"{Fore.GREEN}User: {Style.RESET_ALL}{message}")
        print(f"{Fore.CYAN}({description}){Style.RESET_ALL}")
        
        response = await orchestrator.delegate_task("chat_interface", {
            "action": "chat",
            "message": message
        })
        
        if response.success:
            print(f"{Fore.MAGENTA}Assistant: {Style.RESET_ALL}{response.data['response']}\n")
        
        await asyncio.sleep(1)


async def demo_agent_coordination(orchestrator):
    """Demonstrate multi-agent coordination"""
    print_section("Step 5: Multi-Agent Coordination")
    
    print("Demonstrating how agents work together...\n")
    await asyncio.sleep(0.5)
    
    print(f"{Fore.YELLOW}Scenario:{Style.RESET_ALL} Checking system health and providing a report\n")
    
    # Step 1: Get CPU status
    print("1. Checking CPU usage...")
    cpu_response = await orchestrator.delegate_task("system_monitor", {"action": "cpu"})
    cpu_usage = cpu_response.data['percent']
    print_success(f"CPU usage: {cpu_usage}%")
    
    await asyncio.sleep(0.5)
    
    # Step 2: Get memory status
    print("\n2. Checking memory usage...")
    mem_response = await orchestrator.delegate_task("system_monitor", {"action": "memory"})
    mem_usage = mem_response.data['virtual']['percent']
    print_success(f"Memory usage: {mem_usage}%")
    
    await asyncio.sleep(0.5)
    
    # Step 3: Count processes
    print("\n3. Counting running processes...")
    proc_response = await orchestrator.delegate_task("task_automation", {"action": "list_processes"})
    proc_count = len(proc_response.data)
    print_success(f"Running processes: {proc_count}")
    
    await asyncio.sleep(0.5)
    
    # Step 4: Generate summary
    print("\n4. Generating health report...")
    await asyncio.sleep(0.5)
    
    print(f"\n{Fore.GREEN}{'─' * 70}")
    print(f"{Fore.YELLOW}System Health Report{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'─' * 70}{Style.RESET_ALL}")
    print_info("CPU Usage", f"{cpu_usage}% {'✓ Normal' if cpu_usage < 80 else '⚠ High'}")
    print_info("Memory Usage", f"{mem_usage}% {'✓ Normal' if mem_usage < 80 else '⚠ High'}")
    print_info("Active Processes", proc_count)
    print_info("Status", f"{Fore.GREEN}System running smoothly!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'─' * 70}{Style.RESET_ALL}")


async def demo_conclusion():
    """Show conclusion"""
    print_section("Demo Complete!")
    
    print(f"{Fore.MAGENTA}You've just seen the AI Administrator in action!{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}What you can do next:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}1.{Style.RESET_ALL} Run 'python main.py' for the interactive CLI")
    print(f"  {Fore.GREEN}2.{Style.RESET_ALL} Run 'python examples.py' for library usage examples")
    print(f"  {Fore.GREEN}3.{Style.RESET_ALL} Read QUICKSTART.md for a quick start guide")
    print(f"  {Fore.GREEN}4.{Style.RESET_ALL} Read README.md for full documentation")
    print(f"  {Fore.GREEN}5.{Style.RESET_ALL} Create your own custom agents!")
    
    print(f"\n{Fore.CYAN}Thank you for exploring AI Administrator! 🎉{Style.RESET_ALL}\n")


async def main():
    """Run the demo"""
    print("\n" * 2)
    
    await demo_introduction()
    orchestrator = await demo_agent_setup()
    await demo_system_monitoring(orchestrator)
    await demo_task_automation(orchestrator)
    await demo_chat_interface(orchestrator)
    await demo_agent_coordination(orchestrator)
    await demo_conclusion()


if __name__ == "__main__":
    asyncio.run(main())
