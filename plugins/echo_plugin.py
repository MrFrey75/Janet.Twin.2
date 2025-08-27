# plugins/echo_plugin.py
from typing import Dict, Any

class EchoPlugin:
    """
    A simple plugin that echoes the user's message.
    """
    def execute(self, payload: Dict[str, Any]) -> str:
        """
        Executes the echo action.

        Args:
            payload: A dictionary containing the data for the plugin to process.
                     It is expected to contain a 'text' key.

        Returns:
            A string containing the echoed text.
        """
        # We use .get() to safely access the 'text' key from the payload.
        # This prevents errors if the key is missing.
        text_to_echo = payload.get("text", "No text provided to echo.")
        return f"Echoing back: {text_to_echo}"
