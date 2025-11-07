"""
Main entry point for AI Administrator
"""

import asyncio
import sys
from colorama import init, Fore, Style
from ai_admin.core.orchestrator import Orchestrator
from ai_admin.agents.system_monitor import SystemMonitorAgent
from ai_admin.agents.task_automation import TaskAutomationAgent
from ai_admin.agents.chat_interface import ChatInterfaceAgent


# Initialize colorama for colored terminal output
init(autoreset=True)


def print_banner():
    """Print welcome banner"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       {Fore.MAGENTA}AI Administrator Assistant{Fore.CYAN}                         ║
║       {Fore.GREEN}Your Personal PC Management Companion{Fore.CYAN}               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)


def print_menu():
    """Print main menu"""
    menu = f"""
{Fore.YELLOW}Available Commands:{Style.RESET_ALL}
  {Fore.GREEN}1.{Style.RESET_ALL} Monitor System     - Check CPU, memory, disk, network
  {Fore.GREEN}2.{Style.RESET_ALL} List Processes     - View running processes
  {Fore.GREEN}3.{Style.RESET_ALL} List Directory     - Browse filesystem
  {Fore.GREEN}4.{Style.RESET_ALL} Chat               - Chat with the assistant
  {Fore.GREEN}5.{Style.RESET_ALL} Agent Status       - View agent status
  {Fore.GREEN}6.{Style.RESET_ALL} Help               - Show this menu
  {Fore.GREEN}0.{Style.RESET_ALL} Exit               - Quit the application
    """
    print(menu)


async def monitor_system(orchestrator: Orchestrator):
    """Monitor system resources"""
    print(f"\n{Fore.CYAN}Monitoring system...{Style.RESET_ALL}")
    response = await orchestrator.delegate_task("system_monitor", {"action": "full_status"})
    
    if response.success:
        data = response.data
        print(f"\n{Fore.GREEN}System Information:{Style.RESET_ALL}")
        print(f"  Platform: {data['platform']['system']} {data['platform']['release']}")
        print(f"  Processor: {data['platform']['processor']}")
        print(f"\n{Fore.YELLOW}CPU:{Style.RESET_ALL}")
        print(f"  Usage: {data['cpu']['percent']}%")
        print(f"  Cores: {data['cpu']['count']} ({data['cpu']['count_physical']} physical)")
        print(f"\n{Fore.YELLOW}Memory:{Style.RESET_ALL}")
        print(f"  Usage: {data['memory']['virtual']['percent']}%")
        print(f"  Used: {data['memory']['virtual']['used'] / (1024**3):.2f} GB")
        print(f"  Available: {data['memory']['virtual']['available'] / (1024**3):.2f} GB")
        print(f"\n{Fore.YELLOW}Disk:{Style.RESET_ALL}")
        for partition in data['disk']['partitions'][:3]:  # Show first 3 partitions
            print(f"  {partition['mountpoint']}: {partition['percent']}% used "
                  f"({partition['free'] / (1024**3):.2f} GB free)")
    else:
        print(f"{Fore.RED}Error: {response.message}{Style.RESET_ALL}")


async def list_processes(orchestrator: Orchestrator):
    """List running processes"""
    print(f"\n{Fore.CYAN}Fetching process list...{Style.RESET_ALL}")
    response = await orchestrator.delegate_task("task_automation", {"action": "list_processes"})
    
    if response.success:
        processes = response.data[:10]  # Show top 10
        print(f"\n{Fore.GREEN}Top Processes:{Style.RESET_ALL}")
        print(f"{'PID':<10} {'Name':<30} {'CPU%':<10} {'Memory%':<10}")
        print("-" * 60)
        for proc in processes:
            print(f"{proc['pid']:<10} {proc['name'][:28]:<30} "
                  f"{proc['cpu_percent']:<10.1f} {proc['memory_percent']:<10.2f}")
    else:
        print(f"{Fore.RED}Error: {response.message}{Style.RESET_ALL}")


async def list_directory(orchestrator: Orchestrator):
    """List directory contents"""
    path = input(f"\n{Fore.CYAN}Enter directory path (or press Enter for current): {Style.RESET_ALL}").strip()
    if not path:
        import os
        path = os.getcwd()
        
    response = await orchestrator.delegate_task("task_automation", {
        "action": "list_directory",
        "path": path
    })
    
    if response.success:
        data = response.data
        print(f"\n{Fore.GREEN}Contents of {data['path']}:{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Directories ({len(data['directories'])}):{Style.RESET_ALL}")
        for d in data['directories'][:10]:
            print(f"  📁 {d}")
        print(f"\n{Fore.YELLOW}Files ({len(data['files'])}):{Style.RESET_ALL}")
        for f in data['files'][:10]:
            print(f"  📄 {f}")
        if len(data['files']) > 10 or len(data['directories']) > 10:
            print(f"\n  ... and {data['total_items'] - 20} more items")
    else:
        print(f"{Fore.RED}Error: {response.message}{Style.RESET_ALL}")


async def chat_with_assistant(orchestrator: Orchestrator):
    """Chat with the assistant"""
    print(f"\n{Fore.CYAN}Chat with AI Administrator (type 'exit' to return to menu){Style.RESET_ALL}\n")
    
    while True:
        user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
        
        if user_input.lower() in ['exit', 'quit', 'back']:
            break
            
        if not user_input:
            continue
            
        response = await orchestrator.delegate_task("chat_interface", {
            "action": "chat",
            "message": user_input
        })
        
        if response.success:
            print(f"{Fore.MAGENTA}Assistant: {Style.RESET_ALL}{response.data['response']}\n")
        else:
            print(f"{Fore.RED}Error: {response.message}{Style.RESET_ALL}\n")


async def show_agent_status(orchestrator: Orchestrator):
    """Show status of all agents"""
    status = orchestrator.get_status()
    print(f"\n{Fore.GREEN}Agent Status:{Style.RESET_ALL}")
    print(f"  Total Agents: {status['total_agents']}")
    print(f"  Enabled: {status['enabled_agents']}")
    print(f"\n{Fore.YELLOW}Agents:{Style.RESET_ALL}")
    for name, info in status['agents'].items():
        status_icon = "✓" if info['enabled'] else "✗"
        status_color = Fore.GREEN if info['enabled'] else Fore.RED
        print(f"  {status_color}{status_icon}{Style.RESET_ALL} {name}: {info['description']}")


async def main():
    """Main application loop"""
    print_banner()
    
    # Initialize orchestrator and agents
    orchestrator = Orchestrator()
    
    # Register agents
    print(f"\n{Fore.CYAN}Initializing agents...{Style.RESET_ALL}")
    orchestrator.register_agent(SystemMonitorAgent())
    orchestrator.register_agent(TaskAutomationAgent())
    orchestrator.register_agent(ChatInterfaceAgent())
    
    print(f"\n{Fore.GREEN}All agents initialized successfully!{Style.RESET_ALL}")
    print_menu()
    
    # Main loop
    while True:
        try:
            choice = input(f"\n{Fore.CYAN}Enter command number: {Style.RESET_ALL}").strip()
            
            if choice == "0":
                print(f"\n{Fore.YELLOW}Goodbye! Thanks for using AI Administrator.{Style.RESET_ALL}\n")
                break
            elif choice == "1":
                await monitor_system(orchestrator)
            elif choice == "2":
                await list_processes(orchestrator)
            elif choice == "3":
                await list_directory(orchestrator)
            elif choice == "4":
                await chat_with_assistant(orchestrator)
            elif choice == "5":
                await show_agent_status(orchestrator)
            elif choice == "6":
                print_menu()
            else:
                print(f"{Fore.RED}Invalid choice. Please enter a number from 0-6.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted. Exiting...{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    asyncio.run(main())
