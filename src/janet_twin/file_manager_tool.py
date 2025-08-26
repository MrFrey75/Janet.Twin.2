# file_manager_tool.py
from PyQt6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class FileManagerTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel("Files Uploaded")
        layout.addWidget(label)

        file_list = QListWidget()
        file_list.addItem("document.pdf")
        file_list.addItem("notes.txt")
        layout.addWidget(file_list)