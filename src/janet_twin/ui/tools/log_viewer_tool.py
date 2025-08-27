#

import os, re
from PyQt6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor
from src.janet_twin.utils.logger_utility import logger


class LogViewerTool(QWidget):
    REFRESH_INTERVAL_MS = 2000  # Refresh every 2 seconds

    # Define color mappings for different log levels.
    # Note: It's good practice to make the log level keywords all uppercase for reliable detection.
    LOG_COLORS = {
        "DEBUG": QColor("gray"),
        "INFO": QColor("blue"),
        "WARNING": QColor("orange"),
        "ERROR": QColor("red"),
        "CRITICAL": QColor("purple"),
        "MESSAGE": QColor("yellow"),
    }



    def __init__(self):
        super().__init__()

        self.log_dir = os.path.join(os.path.dirname(__file__), 'logs')
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
        return self.LOG_COLORS.get(severity)

    def load_log(self):
        """
        Load log contents into the QTextEdit and apply color coding.
        This method now reads the file line by line and uses a QTextCursor
        to apply formatting (colors) to each line before inserting it.
        """

        self.log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        self.log_file_path = os.path.join(self.log_dir, 'event.log')

        if not os.path.exists(self.log_file_path):
            self.log_display.setPlaceholderText(f"No log found at {self.log_file_path}")
            return

        with open(self.log_file_path, "r") as f:
            lines = f.readlines()

        doc = self.log_display.document()
        cursor = QTextCursor(doc)

        # Clear existing content before adding new.
        # This is necessary to avoid duplicating log entries on each refresh.
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.removeSelectedText()

        # Process and format each line individually.
        for line in lines:

            try:
                format = QTextCharFormat()

                log_arr = line.split(" - ")

                date = log_arr[0]
                severity = log_arr[2]
                message = re.sub(r'\n', '', log_arr[3])
                color = self.return_severity_color(severity)

                format.setForeground(color)

                # Insert the line with the determined format.
                cursor.insertText(f"{date} - {message}", format)

            except IndexError:
                logger.warning(f"Error processing line: '{severity} - {date} - {message}'. It may not have the expected format.")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

        # Scroll to the bottom to show the latest logs.
        # We move the cursor to the end and ensure the text edit follows it.
        self.log_display.moveCursor(QTextCursor.MoveOperation.End)