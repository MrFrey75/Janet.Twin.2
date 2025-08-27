# File: conversation_history_tool.py
import os
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget, QListWidgetItem, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QFileSystemWatcher

from src.janet_twin.utils.logger_utility import logger
from src.janet_twin.utils.conversation_utility import ConversationUtility

# Define the conversation path as it's used to list all files
CONVERSATION_PATH = os.path.join("data", "conversations")


class ConversationHistoryTool(QWidget):
    # Define a new signal that will emit the unique ID of the conversation
    conversation_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.conv_utility = ConversationUtility()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Conversation History")
        layout.addWidget(label)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_history)
        layout.addWidget(self.refresh_button)

        self.history_list = QListWidget()
        self.load_history()
        layout.addWidget(self.history_list)



        # Connect the list widget's itemClicked signal to a handler
        self.history_list.itemClicked.connect(self.on_item_clicked)

        watcher = QFileSystemWatcher()
        watcher.addPath(CONVERSATION_PATH)
        watcher.directoryChanged.connect(self.refresh_history)

    def load_history(self):
        """
        Loads and displays the conversation history from individual YAML files.
        """
        self.history_list.clear()

        if os.path.exists(CONVERSATION_PATH):
            for filename in os.listdir(CONVERSATION_PATH):
                if filename.endswith(".yaml"):
                    unique_id = os.path.splitext(filename)[0]
                    conversation_data = self.conv_utility.load_conversation(unique_id)

                    if conversation_data:
                        title = conversation_data.get("title", "Untitled Conversation")
                        # Store the unique_id in the QListWidgetItem's data for easy retrieval
                        item = QListWidgetItem(f"{title}")
                        item.setData(Qt.ItemDataRole.UserRole, unique_id)
                        self.history_list.addItem(item)
                    else:
                        logger.warning(f"Failed to load data for file: {filename}")
        else:
            self.history_list.addItem("No conversation history found.")

    def on_item_clicked(self, item):
        """
        Handler for when a history item is clicked.
        Emits the unique ID of the selected conversation.
        """
        unique_id = item.data(Qt.ItemDataRole.UserRole)
        if unique_id:
            logger.debug(f"Conversation with UUID {unique_id} selected from history.")
            self.conversation_selected.emit(unique_id)

    def refresh_history(self):
        """
        Slot to refresh the conversation history list.
        """
        logger.info("Refreshing conversation history list.")
        self.load_history()