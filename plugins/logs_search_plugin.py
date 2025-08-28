import os
import requests
from typing import Dict, Any

class LogsSearch:
    """
    A plugin for searching logs.
    """

    def __init__(self):
        self.log_dir = None
        self.log_file = None
        self.log_path = None

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