import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QLabel,
    QDockWidget,
    QListWidget,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QPushButton,
    QTextEdit,
    QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import random

class GPTClientUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Conversational GPT Client")
        self.setGeometry(100, 100, 1200, 800)

        # --- Toolbar ---
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; }")

        self.new_chat_action = QAction("New Chat", self)
        self.toolbar.addAction(self.new_chat_action)
        self.toolbar.addSeparator()

        # --- Tool actions ---
        self.tool_actions = []
        for i in range(1, 5):
            action = QAction(f"Tool {i}", self)
            self.toolbar.addAction(action)
            action.triggered.connect(lambda checked, a=action: self.show_toolbox(a.text()))
            self.tool_actions.append(action)

        self.toolbar.addSeparator()

        # --- Settings action ---
        self.settings_action = QAction("Settings", self)
        self.toolbar.addAction(self.settings_action)
        self.settings_action.triggered.connect(lambda: self.show_toolbox("Settings"))

        # --- Main chat area ---
        self.main_area = QWidget()
        self.main_layout = QVBoxLayout(self.main_area)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Scrollable chat area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_container.setLayout(self.chat_layout)
        self.chat_scroll.setWidget(self.chat_container)
        self.main_layout.addWidget(self.chat_scroll)

        # Input area
        self.input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a message...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.send_button)
        self.main_layout.addLayout(self.input_layout)

        self.setCentralWidget(self.main_area)

        # --- Right-side collapsible dock ---
        self.toolbox_dock = QDockWidget("Toolbox", self)
        self.toolbox_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.toolbox_dock.setFloating(False)
        self.toolbox_dock.setVisible(False)
        self.toolbox_widget = QWidget()
        self.toolbox_layout = QVBoxLayout(self.toolbox_widget)
        self.toolbox_widget.setLayout(self.toolbox_layout)
        self.toolbox_dock.setWidget(self.toolbox_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.toolbox_dock)

    # --- Tool / Settings dock ---
    def show_toolbox(self, name):
        self.toolbox_dock.setWindowTitle(name)

        # Clear previous contents
        for i in reversed(range(self.toolbox_layout.count())):
            self.toolbox_layout.itemAt(i).widget().setParent(None)

        if name == "Settings":
            self.add_settings_widgets()
        else:
            for i in range(1, 6):
                label = QLabel(f"{name} Option {i}")
                self.toolbox_layout.addWidget(label)

        self.toolbox_dock.setVisible(True)
        self.toolbox_dock.raise_()

    # --- Settings widgets ---
    def add_settings_widgets(self):
        username_label = QLabel("User Name:")
        username_input = QLineEdit()
        self.toolbox_layout.addWidget(username_label)
        self.toolbox_layout.addWidget(username_input)

        notifications_checkbox = QCheckBox("Enable Notifications")
        self.toolbox_layout.addWidget(notifications_checkbox)

        theme_label = QLabel("Theme:")
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark", "System"])
        self.toolbox_layout.addWidget(theme_label)
        self.toolbox_layout.addWidget(theme_combo)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(lambda: self.save_settings(username_input, notifications_checkbox, theme_combo))
        self.toolbox_layout.addWidget(save_button)

    def save_settings(self, username_input, notifications_checkbox, theme_combo):
        username = username_input.text()
        notifications = notifications_checkbox.isChecked()
        theme = theme_combo.currentText()
        print(f"Settings Saved → Username: {username}, Notifications: {notifications}, Theme: {theme}")

    # --- Chat functionality ---
    def send_message(self):
        text = self.input_line.text().strip()
        if not text:
            return

        # Add user message
        self.add_chat_bubble("You", text)
        self.input_line.clear()

        # Mock GPT response
        response = self.mock_gpt_response(text)
        self.add_chat_bubble("GPT", response)

    def add_chat_bubble(self, sender, text):
        bubble = QLabel(f"<b>{sender}:</b> {text}")
        bubble.setWordWrap(True)
        bubble.setStyleSheet(
            "border: 1px solid #ccc; border-radius: 8px; padding: 6px; margin: 4px;"
            + ("background-color: #e0f7fa;" if sender == "You" else "background-color: #fff9c4;")
        )
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.chat_layout.addWidget(bubble)
        # Auto-scroll to bottom
        self.chat_scroll.verticalScrollBar().setValue(self.chat_scroll.verticalScrollBar().maximum())

    def mock_gpt_response(self, user_text):
        # Very simple mock GPT responses
        responses = [
            "Interesting! Can you tell me more?",
            "I see, go on...",
            "That's a great point!",
            "Hmm, let's think about that.",
            "Can you clarify what you mean?"
        ]
        return random.choice(responses)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPTClientUI()
    window.show()
    sys.exit(app.exec())
