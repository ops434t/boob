# AI Administrator Assistant 🤖

Your perfect AI-powered PC administrator companion built with intelligent agents!

## Overview

AI Administrator is an agent-based system that helps you manage and monitor your PC with the power of AI. It uses multiple specialized agents that work together to provide system monitoring, task automation, and conversational assistance.

## Features

✨ **Multi-Agent Architecture**
- **System Monitor Agent**: Tracks CPU, memory, disk, and network usage
- **Task Automation Agent**: Automates common system administration tasks
- **Chat Interface Agent**: Provides conversational interaction
- **Orchestrator**: Coordinates all agents seamlessly

🖥️ **System Monitoring**
- Real-time CPU usage and information
- Memory (RAM) usage and swap status
- Disk space and I/O statistics
- Network traffic monitoring
- Platform and processor information

⚙️ **Task Automation**
- List running processes
- Browse filesystem directories
- View environment variables
- Safe and controlled task execution

💬 **Conversational Interface**
- Chat with your AI administrator
- Natural language understanding
- Helpful responses and guidance
- Conversation history tracking

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ops434t/boob.git
cd boob
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Interactive CLI

```bash
python main.py
```

This launches an interactive menu where you can:
1. Monitor your system resources
2. View running processes
3. Browse directories
4. Chat with the AI assistant
5. Check agent status

### Using as a Library

```python
import asyncio
from ai_admin.core.orchestrator import Orchestrator
from ai_admin.agents.system_monitor import SystemMonitorAgent

async def example():
    # Create orchestrator
    orchestrator = Orchestrator()
    
    # Register agents
    orchestrator.register_agent(SystemMonitorAgent())
    
    # Execute tasks
    response = await orchestrator.delegate_task(
        "system_monitor",
        {"action": "cpu"}
    )
    
    print(response.data)

asyncio.run(example())
```

## Architecture

```
AI Administrator
├── Core Framework
│   ├── Agent (Base class)
│   ├── AgentResponse (Response structure)
│   └── Orchestrator (Agent coordinator)
│
└── Specialized Agents
    ├── SystemMonitorAgent
    ├── TaskAutomationAgent
    └── ChatInterfaceAgent
```

### Agent Communication

Agents communicate through the Orchestrator using a simple task-response pattern:
- Tasks are dictionaries with an `action` key and optional parameters
- Responses are `AgentResponse` objects with `success`, `data`, `message`, and `agent_name`

## Example Interactions

### Monitoring System
```python
task = {"action": "full_status"}
response = await orchestrator.delegate_task("system_monitor", task)
# Returns complete system information
```

### Chatting with Assistant
```python
task = {"action": "chat", "message": "Hello!"}
response = await orchestrator.delegate_task("chat_interface", task)
# Returns conversational response
```

### Listing Processes
```python
task = {"action": "list_processes"}
response = await orchestrator.delegate_task("task_automation", task)
# Returns list of running processes
```

## Development

### Adding New Agents

1. Create a new agent class inheriting from `Agent`:
```python
from ai_admin.core.agent import Agent, AgentResponse

class MyCustomAgent(Agent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="Does amazing things"
        )
    
    async def execute(self, task):
        # Your agent logic here
        return AgentResponse(
            success=True,
            data={"result": "success"},
            message="Task completed",
            agent_name=self.name
        )
```

2. Register it with the orchestrator:
```python
orchestrator.register_agent(MyCustomAgent())
```

### Project Structure

```
boob/
├── ai_admin/              # Main package
│   ├── __init__.py
│   ├── core/             # Core framework
│   │   ├── agent.py      # Base agent class
│   │   └── orchestrator.py
│   └── agents/           # Agent implementations
│       ├── system_monitor.py
│       ├── task_automation.py
│       └── chat_interface.py
├── main.py               # CLI application
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Requirements

- Python 3.7+
- psutil (system monitoring)
- colorama (colored terminal output)
- asyncio (async support)

## Security

The AI Administrator implements several security measures:
- Limited command execution (whitelist approach)
- No direct shell access
- Safe directory browsing with validation
- Environment variable filtering
- Process listing without modification capabilities

## Future Enhancements

- [ ] Integration with AI models (OpenAI, Anthropic) for smarter responses
- [ ] Scheduled task execution
- [ ] Alert system for resource thresholds
- [ ] Web-based dashboard
- [ ] Plugin system for custom agents
- [ ] Configuration file support
- [ ] Logging and audit trails

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this project however you'd like!

## Acknowledgments

Built with ❤️ as a demonstration of agent-based AI systems for PC administration.