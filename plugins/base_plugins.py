import os
from typing import Dict, Any
import requests


class LogsSearch:
    """
    A plugin for searching logs.
    """

    def execute(self, payload: Dict[str, Any]) -> str:
        """
        Executes the log search based on the user's query.

        Args:
            payload (Dict[str, Any]): A dictionary containing the user's
                                      search query under the key "text".

        Returns:
            str: A formatted string of the search results or an error message.
        """
        # Use consistent log path - same as logger_utility.py
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_dir = os.path.join(PROJECT_ROOT, 'logs')
        self.log_file = "event.log"
        self.log_path = os.path.join(self.log_dir, self.log_file)

        user_query = payload.get("text", "")
        if not user_query:
            return "No search query provided."

        if not os.path.exists(self.log_path):
            return f"Error: No log file found at {self.log_path}"

        # Read all lines from the log file.
        with open(self.log_path, "r") as f:
            lines = f.readlines()

        # Search for lines containing the user's query.
        # This list comprehension is a concise way to filter the lines.

        matching_lines = [line.strip() for line in lines if user_query.lower() in line.lower()]

        # Check if any matching lines were found.
        if matching_lines:
            # Join the matching lines into a single string with newlines.

            results = ""

            for line in matching_lines:
                results += line + "\n\n"


            return "\n" + results
        else:
            return f"No logs found containing '{user_query}'."


class GoogleSearchPlugin:
    """
    A plugin for performing Google searches.
    """
    def execute(self, payload: Dict[str, Any]) -> str:
        """
        Provides a response based on the user's search query.

        Args:
                payload: A dictionary containing the data for the plugin.

        Returns:

            A string with the search result.
        """
        GOOGLE_SEARCH_API = "https://www.googleapis.com/customsearch/v1"
        API_KEY = "AIzaSyAOIIoJUoEMvD7qOUEYKkewSRinxYYNhdo"  # Replace with actual API key
        SEARCH_ENGINE_ID = "51feee7a93400443e"  # Replace with actual search engine ID

        user_query = payload.get("text", "")
        if not user_query:
            return "No search query provided"

        try:
            params = {
                'key': API_KEY,
                'cx': SEARCH_ENGINE_ID,
                'q': user_query
            }
            response = requests.get(GOOGLE_SEARCH_API, params=params)
            response.raise_for_status()

            results = response.json()
            if 'items' not in results:
                return "No results found"

            summary = []
            for item in results['items'][:3]:
                summary.append(f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}\n")

            return "\n".join(summary)

        except requests.RequestException as e:
            return f"Error performing search: {str(e)}"


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