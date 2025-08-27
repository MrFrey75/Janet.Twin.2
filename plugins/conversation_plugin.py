# plugins/conversation_plugin.py
from typing import Dict, Any

class ConversationPlugin:
    """
    A simple plugin for handling mock conversational requests.
    """
    def execute(self, payload: Dict[str, Any]) -> str:
        """
        Provides a mock response based on the user's input.

        Args:
            payload: A dictionary containing the data for the plugin.
                     It is expected to have a 'text' key.

        Returns:
            A string with a mock conversational response.
        """
        user_message = payload.get("text", "").lower()

        if "hello" in user_message or "hi" in user_message:
            return "Hello there! How can I assist you today?"
        elif "how are you" in user_message:
            return "I'm doing great, thanks for asking! I am ready to help you."
        elif "who are you" in user_message:
            return "I am an assistant designed to help with tasks like this. I am powered by a Python orchestrator and plugins."
        else:
            return "I'm sorry, I don't understand that. Please try asking about 'hello', 'how are you', or 'who are you'."

