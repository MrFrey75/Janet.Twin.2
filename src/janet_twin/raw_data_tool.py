# raw_data_tool.py
from PyQt6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class RawDataTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Raw Streaming Data (last 1000 lines)")
        layout.addWidget(label)

        raw_data_display = QTextEdit()
        raw_data_display.setReadOnly(True)
        raw_data_display.setPlaceholderText("Raw data will stream here...")
        layout.addWidget(raw_data_display)