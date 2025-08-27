import os
import yaml
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from src.janet_twin.logger import logger
from src.janet_twin.utils.settings_utility import SettingsUtility
from src.janet_twin.utils.conversation_utility import ConversationUtility

# Define the conversation path as it's used to list all files
CONVERSATION_PATH = os.path.join("data", "conversations")


class ConversationHistoryTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Conversation History")
        layout.addWidget(label)

        history_list = QListWidget()
        self.load_history(history_list)
        layout.addWidget(history_list)

    def load_history(self, history_list):
        """
        Loads and displays the conversation history from individual YAML files.
        """
        history_list.clear()

        # Initialize ConversationUtility to load data
        conv_utility = ConversationUtility()

        # Iterate over all files in the conversation directory
        if os.path.exists(CONVERSATION_PATH):
            for filename in os.listdir(CONVERSATION_PATH):
                if filename.endswith(".yaml"):
                    unique_id = os.path.splitext(filename)[0]
                    # The fix is here. The method signature expects `self` and `unique_id`.
                    # The correct call is conv_utility.load_conversation(unique_id)
                    # if load_conversation were an instance method.
                    # Since it is a static method in the original file, it should be called as such.
                    # This is likely a copy-paste error in the original code.
                    # The correct call should not pass `conv_utility` twice
                    conversation_data = ConversationUtility.load_conversation(unique_id)

                    if conversation_data:
                        title = conversation_data.get("title", "Untitled Conversation")
                        last_updated = conversation_data.get("last_updated", "N/A")

                        # Add a new item to the list with the title and timestamp
                        history_list.addItem(f"{title}: {last_updated}")
                    else:
                        logger.warning(f"Failed to load data for file: {filename}")
        else:
            history_list.addItem("No conversation history found.")