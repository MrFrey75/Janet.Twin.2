# The following script requires PyQt6 to be installed.
# You can install it using pip: pip install PyQt6

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QLabel,
)
from PyQt6.QtGui import QAction


class GPTClientUI(QMainWindow):
    """
    The main application window for the GPT client UI.
    This class sets up the core layout with a top toolbar and a main chat area.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Conversational GPT Client")
        self.setGeometry(100, 100, 1200, 800)

        # --- Create a top toolbar ribbon with specified functionality ---
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Adding a bit of style to the toolbar for better visibility
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; }")

        # Add the 'New Chat' action
        self.new_chat_action = QAction("New Chat", self)
        self.toolbar.addAction(self.new_chat_action)

        # Add the first separator
        self.toolbar.addSeparator()

        # Add placeholder actions for the tools
        self.tool1_action = QAction("Tool 1", self)
        self.toolbar.addAction(self.tool1_action)
        self.tool2_action = QAction("Tool 2", self)
        self.toolbar.addAction(self.tool2_action)
        self.tool3_action = QAction("Tool 3", self)
        self.toolbar.addAction(self.tool3_action)
        self.tool4_action = QAction("Tool 4", self)
        self.toolbar.addAction(self.tool4_action)

        # Add the second separator
        self.toolbar.addSeparator()

        # Add the 'Settings' action
        self.settings_action = QAction("Settings", self)
        self.toolbar.addAction(self.settings_action)

        # --- Create the main chat area ---
        self.main_area = QWidget()
        self.main_area_layout = QVBoxLayout(self.main_area)
        self.main_area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a placeholder for the chat interface
        chat_label = QLabel("Main Chat Area (Placeholder)")
        chat_label.setStyleSheet("font-size: 24px; color: #888;")
        self.main_area_layout.addWidget(chat_label)

        # Set the main chat area as the central widget
        self.setCentralWidget(self.main_area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPTClientUI()
    window.show()
    sys.exit(app.exec())
