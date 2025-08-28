# plugins/base_plugins.py

import os
from typing import Dict, Any
import requests
import ollama
import ollama.errors



class ConversationPlugin:
    """
    A simple plugin for handling mock conversational requests.
    """
    def execute(self, payload: Dict[str, Any]) -> str:
        """
        Provides a response using an Ollama model based on the user's input.

        Args:
            payload: A dictionary containing the data for the plugin.
                     It is expected to have a 'text' key and 'conversation_history'.

        Returns:
            A string with a conversational response from the Ollama model.
        """
        try:
            conversation_history = payload.get("conversation_history", [])
            response = ollama.chat(
                model='llama3',
                messages=conversation_history
            )
            return response['message']['content']
        except ollama.errors.ResponseError as e:
            return f"Ollama API Error: {str(e)}. Please check your model configuration."
        except requests.exceptions.ConnectionError as e:
            return f"Error: Could not connect to Ollama. Please ensure the server is running. ({str(e)})"
        except Exception as e:
            return f"An unexpected error occurred with the Ollama plugin: {str(e)}"