# File: main_window.py
import os
import yaml
from datetime import datetime
from uuid import uuid4

from PyQt6.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QScrollArea, QSizePolicy
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from src.janet_twin.logger import logger
from src.janet_twin.utils.settings_utility import SettingsUtility
from src.janet_twin.utils.conversation_utility import ConversationUtility
from src.janet_twin.models.conversation import Conversation
from .toolbox import ToolboxDock
from .chat import ChatArea
from src.janet_twin.orchestrator.orchestrator import Orchestrator
from src.janet_twin.orchestrator.registry import PluginRegistry
from src.janet_twin.models.task import Task
from plugins.echo_plugin import EchoPlugin
from plugins.base_plugins import ConversationPlugin, GoogleSearchPlugin

class GPTClientUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings_utility = SettingsUtility()
        self.settings_utility.load_settings()
        self.settings = self.settings_utility.expose_settings()

        self.conversation_utility = ConversationUtility()
        self.current_conversation = None

        self.assistant_name = self.settings.get("assistant-name", "JANET")
        self.username = self.settings.get("username", "You")

        self.setWindowTitle(self.assistant_name + " - GPT Client")
        self.setGeometry(100, 100, 1200, 800)

        self.plugin_registry = PluginRegistry()
        self.orchestrator = Orchestrator(self.plugin_registry)
        self.plugin_registry.register("echo", EchoPlugin())
        self.plugin_registry.register("search", GoogleSearchPlugin())
        self.plugin_registry.register("conversation", ConversationPlugin())

        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; }")

        self.new_chat_action = QAction("New Chat", self)
        self.toolbar.addAction(self.new_chat_action)
        self.toolbar.addSeparator()
        self.new_chat_action.triggered.connect(self.start_new_conversation)

        tool_names = ["Conversation History", "File Manager", "Log Viewer", "Raw Data"]
        self.tool_actions = []
        for name in tool_names:
            action = QAction(name, self)
            self.toolbar.addAction(action)
            self.tool_actions.append(action)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)

        self.settings_action = QAction(QIcon.fromTheme("preferences-system"), "Settings", self)
        self.toolbar.addAction(self.settings_action)

        self.main_area = QWidget()
        self.main_layout = QVBoxLayout(self.main_area)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_scroll.setWidget(self.chat_container)
        self.main_layout.addWidget(self.chat_scroll)

        self.input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a message...")
        self.send_button = QPushButton("Send")
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.send_button)
        self.main_layout.addLayout(self.input_layout)

        self.setCentralWidget(self.main_area)

        self.chat_area = ChatArea(self.chat_layout, self.chat_scroll)
        self.send_button.clicked.connect(self.send_message)

        self.start_new_conversation()

        self.toolbox = ToolboxDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.toolbox)
        for action in self.tool_actions:
            action.triggered.connect(lambda checked, a=action: self.toolbox.show_toolbox(a.text()))
        self.settings_action.triggered.connect(lambda: self.toolbox.show_toolbox("Settings"))

        # Connect the conversation_selected signal from the toolbox to the new handler
        self.toolbox.get_tool("Conversation History").conversation_selected.connect(self.load_conversation_by_id)

    def start_new_conversation(self):
        """
        Saves the current conversation and initializes a new one.
        """
        if self.current_conversation and self.current_conversation.messages:
            self.save_current_conversation()

        self.current_conversation = Conversation()
        logger.info(f"New conversation started with UUID: {self.current_conversation.unique_id}")

        self.chat_area.clear_chat()
        self.setWindowTitle("New Chat - GPT Client")

    def save_current_conversation(self):
        """
        Saves the current conversation to a YAML file, updating the last_updated timestamp.
        """
        if self.current_conversation and self.current_conversation.messages:
            self.current_conversation.last_updated = datetime.now()

            if not self.current_conversation.title and self.current_conversation.messages:
                first_message_text = self.current_conversation.messages[0].get("text", "Untitled")
                self.current_conversation.title = f"'{first_message_text[:30]}...'"

            self.conversation_utility.save_conversation(str(self.current_conversation.unique_id),
                                                        self.current_conversation.to_dict())
            logger.info(f"Conversation '{self.current_conversation.title}' saved to registry.")

    def load_conversation_by_id(self, unique_id: str):
        """
        Loads a conversation by its unique ID and displays it in the chat window.
        """
        # Save the current conversation before switching
        self.save_current_conversation()

        conversation_data = self.conversation_utility.load_conversation(unique_id)
        if conversation_data:
            # Re-initialize the Conversation object from the loaded data
            self.current_conversation = Conversation(
                unique_id=unique_id,
                created_at=datetime.fromisoformat(conversation_data.get("created_at")),
                last_updated=datetime.fromisoformat(conversation_data.get("last_updated")),
                filename=conversation_data.get("filename", ""),
                title=conversation_data.get("title", "Untitled"),
                messages=conversation_data.get("messages", [])
            )
            logger.info(f"Loaded conversation with UUID: {self.current_conversation.unique_id}")
            self.setWindowTitle(f"{self.current_conversation.title} - GPT Client")

            # Clear the existing chat and populate with the loaded messages
            self.chat_area.clear_chat()
            for message in self.current_conversation.messages:
                sender = self.username if message["role"] == "user" else self.assistant_name
                self.chat_area.add_chat_bubble(sender, message["text"])
        else:
            logger.warning(f"Could not load conversation with unique ID: {unique_id}")


    def send_message(self):
        text = self.input_line.text().strip()
        if not text:
            return

        self.chat_area.add_chat_bubble(self.username, text)
        self.current_conversation.messages.append({"role": "user", "text": text})
        logger.info(f"{self.username}: {text}")
        self.input_line.clear()

        self.save_current_conversation()

        command = None
        payload_text = text

        if ":" in text:
            parts = text.split(":", 1)
            command = parts[0].strip().lower()
            payload_text = parts[1].strip()

        if not command or not self.plugin_registry.get(command):
            command = "conversation"
            payload_text = text

        payload = {"text": payload_text, "conversation_history": self.current_conversation.messages}
        task = Task(user=self.username, command=command, payload=payload)

        response = self.orchestrator.handle(task)

        self.chat_area.add_chat_bubble(self.assistant_name, response)
        self.current_conversation.messages.append({"role": "assistant", "text": response})
        logger.info(f"{self.assistant_name}: {response}")

        self.save_current_conversation()