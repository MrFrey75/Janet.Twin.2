# main_window.py
from PyQt6.QtWidgets import QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea, QSizePolicy
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from src.janet_twin.logger import logger
# Import the SettingsUtility class
from src.janet_twin.utils.settings_utility import SettingsUtility

# Corrected import statement
from .toolbox import ToolboxDock
from .chat import ChatArea

assistant_name = "JANET"
username = "You"

class GPTClientUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize and load settings
        self.settings_utility = SettingsUtility()
        self.settings_utility.load_settings()
        self.settings = self.settings_utility.expose_settings()

        assistant_name = self.settings.get("assistant-name", "JANET")
        username = self.settings.get("username", "You")

        self.setWindowTitle(assistant_name + " - GPT Client")
        self.setGeometry(100, 100, 1200, 800)

        # Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; }")

        self.new_chat_action = QAction("New Chat", self)
        self.toolbar.addAction(self.new_chat_action)
        self.toolbar.addSeparator()

        # Tool buttons
        tool_names = ["Conversation History", "File Manager", "Log Viewer", "Raw Data"]
        self.tool_actions = []
        for name in tool_names:
            action = QAction(name, self)
            self.toolbar.addAction(action)
            self.tool_actions.append(action)

        # Create a spacer widget to push the settings icon to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)

        # Settings with gear icon
        self.settings_action = QAction(QIcon.fromTheme("preferences-system"), "Settings", self)
        self.toolbar.addAction(self.settings_action)

        # Main chat area
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

        # Input line and send button
        self.input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a message...")
        self.send_button = QPushButton("Send")
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.send_button)
        self.main_layout.addLayout(self.input_layout)

        self.setCentralWidget(self.main_area)

        # Chat logic
        self.chat_area = ChatArea(self.chat_layout, self.chat_scroll)
        self.send_button.clicked.connect(self.send_message)

        # Toolbox
        self.toolbox = ToolboxDock(self)
        for action in self.tool_actions:
            action.triggered.connect(lambda checked, a=action: self.toolbox.show_toolbox(a.text()))
        self.settings_action.triggered.connect(lambda: self.toolbox.show_toolbox("Settings"))

    def send_message(self):
        text = self.input_line.text().strip()
        if not text:
            return
        self.chat_area.add_chat_bubble("You", text)

        logger.info(f"{username}: {text}")

        self.input_line.clear()
        response = self.chat_area.mock_gpt_response(text)

        logger.info(f"{assistant_name}: {response}")

        self.chat_area.add_chat_bubble(assistant_name, response)