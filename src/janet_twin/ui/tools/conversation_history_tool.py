# conversation_history_tool.py
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class ConversationHistoryTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Conversation History")
        layout.addWidget(label)

        history_list = QListWidget()
        history_list.addItem("Chat 1: August 26, 2025")
        history_list.addItem("Chat 2: August 25, 2025")
        layout.addWidget(history_list)