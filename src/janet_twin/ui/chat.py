# src/janet_twin/ui/chat.py

from PyQt6.QtWidgets import QLabel, QSizePolicy, QMenu, QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction, QClipboard
from src.janet_twin.utils.settings_utility import SettingsUtility


class ClickableLabel(QLabel):
    """A QLabel that allows text selection and has a context menu to copy."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos: QPoint):
        """Creates and displays a context menu for copying text."""
        menu = QMenu(self)
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy_text)
        menu.addAction(copy_action)
        menu.exec(self.mapToGlobal(pos))

    def copy_text(self):
        """Copies the selected text to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text())


class ChatArea:
    """Handles chat bubbles and mock GPT responses."""

    def __init__(self, chat_layout, chat_scroll):
        self.chat_layout = chat_layout
        self.chat_scroll = chat_scroll

    def add_chat_bubble(self, sender, text):
        bubble = ClickableLabel(f"<b>{sender}:</b> {text}")
        bubble.setWordWrap(True)
        bubble.setStyleSheet(
            "border: 1px solid #ccc; border-radius: 8px; padding: 6px; margin: 4px;"
            + ("background-color: #e0f7fa;" if sender == "You" else "background-color: #fff9c4;")
        )
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.chat_layout.addWidget(bubble)
        # Auto-scroll
        self.chat_scroll.verticalScrollBar().setValue(self.chat_scroll.verticalScrollBar().maximum())

    def clear_chat(self):
        """Removes all chat bubbles from the layout."""
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()