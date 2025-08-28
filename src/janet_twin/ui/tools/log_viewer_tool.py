# File: conversation_history_tool.py
import os, re
from PyQt6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton, QComboBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor
from src.janet_twin.utils.logger_utility import logger, log_message
from logging.handlers import RotatingFileHandler

class LogViewerTool(QWidget):
    REFRESH_INTERVAL_MS = 2000  # Refresh every 2 seconds

    # Define color mappings for different log levels.
    LOG_COLORS = {
        "DEBUG": QColor("gray"),
        "INFO": QColor("blue"),
        "WARNING": QColor("orange"),
        "ERROR": QColor("red"),
        "CRITICAL": QColor("purple"),
        "MESSAGE": QColor("green"),
    }

    def __init__(self):
        super().__init__()

        # Use consistent log path - same as logger_utility.py
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        self.log_dir = os.path.join(PROJECT_ROOT, 'logs')
        self.log_file_path = os.path.join(self.log_dir, 'event.log')

        # Layout setup
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        log_label = QLabel(f"Log File: {self.log_file_path}")
        layout.addWidget(log_label)

        # Optional: manual refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_log)
        layout.addWidget(self.refresh_button)

        # Add filter for log severity
        self.filter_label = QLabel("Filter by Severity:")
        layout.addWidget(self.filter_label)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["ALL", "MESSAGE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.filter_combo.setCurrentText("ALL")

        # Connect the QComboBox to the load_log method
        self.filter_combo.currentIndexChanged.connect(self.load_log)
        layout.addWidget(self.filter_combo)

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

    def return_severity_color(self, severity):
        return self.LOG_COLORS.get(severity, QColor("black"))  # Default to black if severity is unknown

    def load_log(self):
        """
        Load log contents into the QTextEdit and apply color coding.
        This method now reads the file line by line and uses a QTextCursor
        to apply formatting (colors) to each line before inserting it.
        """
        severity_filter = self.filter_combo.currentText()

        if not os.path.exists(self.log_file_path):
            self.log_display.setPlaceholderText(f"No log found at {self.log_file_path}")
            return

        with open(self.log_file_path, "r") as f:
            lines = f.readlines()

        self.log_display.clear()  # Clear content before repopulating

        # We need a cursor to insert formatted text.
        cursor = self.log_display.textCursor()

        # Regex to parse the log line. This is more robust than splitting.
        # It looks for a date, a log level, and the rest of the message.
        log_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - ([A-Z]+) - (.*)$')

        for line in lines:
            match = log_pattern.match(line.strip())

            if match:
                date, severity, message = match.groups()

                # Check for severity filter and skip line if it doesn't match
                if severity_filter != "ALL" and severity != severity_filter:
                    continue

                color_format = QTextCharFormat()
                color = self.return_severity_color(severity)
                color_format.setForeground(color)

                # Insert the formatted log line, including the date and severity,
                # then a newline for proper spacing.
                cursor.insertText(f"{date} - {severity} - {message}\n", color_format)
            else:
                # If a line doesn't match the pattern, it's a raw message.
                # Check if we should display it based on the 'MESSAGE' filter
                if severity_filter == "MESSAGE" or severity_filter == "ALL":
                    color_format = QTextCharFormat()
                    color = self.return_severity_color("MESSAGE")
                    color_format.setForeground(color)
                    cursor.insertText(f"{line.strip()}\n", color_format)

        # Scroll to the bottom to show the latest logs.
        self.log_display.moveCursor(QTextCursor.MoveOperation.End)