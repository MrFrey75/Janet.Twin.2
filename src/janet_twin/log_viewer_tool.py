# log_viewer_tool.py
from PyQt6.QtWidgets import QLabel, QTextEdit, QComboBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class LogViewerTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        log_label = QLabel("Select a Log File:")
        layout.addWidget(log_label)

        log_selector = QComboBox()
        log_selector.addItem("app.log")
        log_selector.addItem("debug.log")
        layout.addWidget(log_selector)

        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setPlaceholderText("Log content will appear here...")
        layout.addWidget(log_display)