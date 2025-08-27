# File: conversation_history_tool.py
import os
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget, QListWidgetItem, QPushButton, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal, QFileSystemWatcher

from src.janet_twin.utils.logger_utility import logger
from src.janet_twin.utils.conversation_utility import ConversationUtility
from datetime import datetime

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

        # order by date created, updated or alphabetical
        self.order_label = QLabel("Order by:")
        layout.addWidget(self.order_label)
        self.order_combo = QComboBox()
        self.order_combo.addItems(["DATE CREATED", "UPDATED", "ALPHABETICAL"])
        self.order_combo.setCurrentText("UPDATED")
        layout.addWidget(self.order_combo)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_history)
        layout.addWidget(self.refresh_button)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        # Connect the QComboBox to reload and sort the history
        self.order_combo.currentIndexChanged.connect(self.load_history)

        self.load_history()

        # Connect the list widget's itemClicked signal to a handler
        self.history_list.itemClicked.connect(self.on_item_clicked)

        watcher = QFileSystemWatcher()
        if os.path.exists(CONVERSATION_PATH):
            watcher.addPath(CONVERSATION_PATH)
            watcher.directoryChanged.connect(self.refresh_history)
        else:
            logger.warning(f"Conversation path does not exist: {CONVERSATION_PATH}")

    def load_history(self):
        """
        Loads, sorts, and displays the conversation history from individual YAML files.
        """
        self.history_list.clear()
        conversations = []

        if not os.path.exists(CONVERSATION_PATH):
            self.history_list.addItem("No conversation history found.")
            return

        for filename in os.listdir(CONVERSATION_PATH):
            if filename.endswith(".yaml"):
                unique_id = os.path.splitext(filename)[0]
                conversation_data = self.conv_utility.load_conversation(unique_id)
                if conversation_data:
                    conversations.append(conversation_data)
                else:
                    logger.warning(f"Failed to load data for file: {filename}")

        # Determine the sort key based on the combo box selection
        sort_by = self.order_combo.currentText()
        if sort_by == "DATE CREATED":
            conversations.sort(key=lambda x: datetime.fromisoformat(x.get("created_at")), reverse=True)
        elif sort_by == "UPDATED":
            conversations.sort(key=lambda x: datetime.fromisoformat(x.get("last_updated")), reverse=True)
        elif sort_by == "ALPHABETICAL":
            conversations.sort(key=lambda x: x.get("title", "").lower())

        if not conversations:
            self.history_list.addItem("No conversation history found.")
            return

        # Populate the QListWidget with the sorted data
        for conv_data in conversations:
            title = conv_data.get("title", "Untitled Conversation")
            unique_id = conv_data.get("unique_id")
            item = QListWidgetItem(f"{title}")
            item.setData(Qt.ItemDataRole.UserRole, unique_id)
            self.history_list.addItem(item)

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