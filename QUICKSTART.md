# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Interactive CLI

```bash
python main.py
```

You'll see a beautiful welcome screen with a menu of options:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║       AI Administrator Assistant                         ║
║       Your Personal PC Management Companion               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Available Commands:
  1. Monitor System     - Check CPU, memory, disk, network
  2. List Processes     - View running processes
  3. List Directory     - Browse filesystem
  4. Chat               - Chat with the assistant
  5. Agent Status       - View agent status
  6. Help               - Show this menu
  0. Exit               - Quit the application
```

### 3. Try Some Commands

**Monitor Your System (Option 1):**
- See real-time CPU usage
- Check memory availability
- View disk space
- Monitor network traffic

**Chat with Your AI Assistant (Option 4):**
```
You: Hello!
Assistant: Hello! I'm your AI Administrator assistant. 
           How can I help you manage your PC today?

You: What can you do?
Assistant: I can help you with:
           - System monitoring (CPU, memory, disk, network)
           - Task automation (file operations, process management)
           - General assistance with PC administration
           Just ask me what you need!
```

**View Running Processes (Option 2):**
See all your running processes with CPU and memory usage.

**Browse Directories (Option 3):**
Navigate your filesystem safely.

## 📚 Using as a Library

Create a file `my_admin.py`:

```python
import asyncio
from ai_admin.core.orchestrator import Orchestrator
from ai_admin.agents.system_monitor import SystemMonitorAgent

async def main():
    # Set up orchestrator
    orchestrator = Orchestrator()
    orchestrator.register_agent(SystemMonitorAgent())
    
    # Monitor CPU
    response = await orchestrator.delegate_task(
        "system_monitor",
        {"action": "cpu"}
    )
    
    print(f"CPU Usage: {response.data['percent']}%")

asyncio.run(main())
```

Run it:
```bash
python my_admin.py
```

## 🎯 Common Use Cases

### 1. Monitor System Health
```python
response = await orchestrator.delegate_task(
    "system_monitor",
    {"action": "full_status"}
)
```

### 2. Check Memory Usage
```python
response = await orchestrator.delegate_task(
    "system_monitor",
    {"action": "memory"}
)
print(f"Memory: {response.data['virtual']['percent']}%")
```

### 3. List Running Processes
```python
response = await orchestrator.delegate_task(
    "task_automation",
    {"action": "list_processes"}
)
for proc in response.data[:10]:
    print(f"{proc['name']}: {proc['cpu_percent']}% CPU")
```

### 4. Chat Interaction
```python
response = await orchestrator.delegate_task(
    "chat_interface",
    {"action": "chat", "message": "Hello!"}
)
print(response.data['response'])
```

## 🛠️ Customization

### Create Your Own Agent

```python
from ai_admin.core.agent import Agent, AgentResponse

class MyCustomAgent(Agent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="My custom functionality"
        )
    
    async def execute(self, task):
        # Your logic here
        return AgentResponse(
            success=True,
            data={"result": "Done!"},
            message="Task completed",
            agent_name=self.name
        )

# Register and use
orchestrator.register_agent(MyCustomAgent())
```

## 🔧 Troubleshooting

**Import Error:**
```bash
pip install -r requirements.txt
```

**Permission Error (Linux/Mac):**
Some system monitoring features may require permissions:
```bash
sudo python main.py
```

**Agent Not Found:**
Make sure the agent is registered:
```python
orchestrator.register_agent(YourAgent())
```

## 📖 Next Steps

1. Run `python examples.py` to see all features in action
2. Read the full README.md for detailed documentation
3. Customize agents for your specific needs
4. Build your own administrator assistant!

## 💡 Tips

- Use the chat interface to ask questions
- Monitor system regularly to catch issues early
- Create custom agents for your specific workflows
- Check agent status to see what's available

Enjoy your AI Administrator! 🎉
