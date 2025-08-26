from PyQt6.QtWidgets import QLabel, QSizePolicy
import random

class ChatArea:
    """Handles chat bubbles and mock GPT responses."""

    def __init__(self, chat_layout, chat_scroll):
        self.chat_layout = chat_layout
        self.chat_scroll = chat_scroll

    def add_chat_bubble(self, sender, text):
        bubble = QLabel(f"<b>{sender}:</b> {text}")
        bubble.setWordWrap(True)
        bubble.setStyleSheet(
            "border: 1px solid #ccc; border-radius: 8px; padding: 6px; margin: 4px;"
            + ("background-color: #e0f7fa;" if sender == "You" else "background-color: #fff9c4;")
        )
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.chat_layout.addWidget(bubble)
        # Auto-scroll
        self.chat_scroll.verticalScrollBar().setValue(self.chat_scroll.verticalScrollBar().maximum())

    def mock_gpt_response(self, user_text):
        responses = [
            "Interesting! Can you tell me more?",
            "I see, go on...",
            "That's a great point!",
            "Hmm, let's think about that.",
            "Can you clarify what you mean?"
        ]
        return random.choice(responses)
