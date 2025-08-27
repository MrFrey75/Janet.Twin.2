# log_viewer_tool.py
from PyQt6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, QTimer
import os

class LogViewerTool(QWidget):
    REFRESH_INTERVAL_MS = 2000  # Refresh every 2 seconds

    def __init__(self):
        super().__init__()

        self.log_file = "janettwin.log"
        self.log_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../logs", self.log_file)
        )

        # Layout setup
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        log_label = QLabel(f"Log File: {self.log_file}")
        layout.addWidget(log_label)

        # Optional: manual refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_log)
        layout.addWidget(self.refresh_button)

        # Log display widget
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        # Timer for auto-refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_log)
        self.timer.start(self.REFRESH_INTERVAL_MS)

        # Initial load
        self.load_log()

    def load_log(self):
        """Load log contents into the QTextEdit."""
        from PyQt6.QtGui import QTextCursor

        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                content = f.read()
            self.log_display.setPlainText(content)
            # Scroll to the bottom to show latest logs
            self.log_display.moveCursor(QTextCursor.MoveOperation.End)
        else:
            self.log_display.setPlaceholderText(f"No log found at {self.log_path}")

