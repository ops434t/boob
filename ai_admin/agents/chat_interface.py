"""
Chat Interface Agent - Provides conversational interface to interact with the system
"""

from typing import Dict, Any, List
from datetime import datetime
from ..core.agent import Agent, AgentResponse


class ChatInterfaceAgent(Agent):
    """Agent for handling chat-based interactions"""
    
    def __init__(self):
        super().__init__(
            name="chat_interface",
            description="Provides conversational interface for user interactions"
        )
        self.conversation_history: List[Dict[str, Any]] = []
        
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        """
        Execute chat interface task
        
        Args:
            task: Task dictionary with 'action' and 'message' keys
            
        Returns:
            AgentResponse with chat response
        """
        action = task.get("action", "chat")
        
        try:
            if action == "chat":
                response = self._handle_chat(task)
            elif action == "history":
                response = self._get_history(task)
            elif action == "clear":
                response = self._clear_history()
            else:
                return AgentResponse(
                    success=False,
                    data=None,
                    message=f"Unknown action: {action}",
                    agent_name=self.name
                )
                
            return AgentResponse(
                success=True,
                data=response,
                message="Chat interaction completed",
                agent_name=self.name
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                data=None,
                message=f"Error in chat interface: {str(e)}",
                agent_name=self.name
            )
            
    def _handle_chat(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a chat message"""
        user_message = task.get("message", "")
        
        # Add user message to history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "message": user_message
        })
        
        # Generate response based on message content
        response_text = self._generate_response(user_message)
        
        # Add response to history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "assistant",
            "message": response_text
        })
        
        return {
            "user_message": user_message,
            "response": response_text,
            "timestamp": datetime.now().isoformat()
        }
        
    def _generate_response(self, message: str) -> str:
        """Generate a response to user message"""
        message_lower = message.lower()
        
        # Simple pattern matching for demo purposes
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm your AI Administrator assistant. How can I help you manage your PC today?"
            
        elif any(word in message_lower for word in ["help", "what can you do"]):
            return ("I can help you with:\n"
                   "- System monitoring (CPU, memory, disk, network)\n"
                   "- Task automation (file operations, process management)\n"
                   "- General assistance with PC administration\n"
                   "Just ask me what you need!")
            
        elif any(word in message_lower for word in ["status", "system", "health"]):
            return "I can check your system status. Ask me to monitor your CPU, memory, disk, or network!"
            
        elif any(word in message_lower for word in ["thank", "thanks"]):
            return "You're welcome! Let me know if you need anything else."
            
        else:
            return (f"I understand you said: '{message}'. "
                   "I'm here to help with system administration. "
                   "You can ask me about system status, monitoring, or automation tasks!")
        
    def _get_history(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get conversation history"""
        limit = task.get("limit", 10)
        return {
            "history": self.conversation_history[-limit:],
            "total_messages": len(self.conversation_history)
        }
        
    def _clear_history(self) -> Dict[str, Any]:
        """Clear conversation history"""
        count = len(self.conversation_history)
        self.conversation_history = []
        return {
            "cleared": count,
            "message": f"Cleared {count} messages from history"
        }
