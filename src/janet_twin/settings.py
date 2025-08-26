from PyQt6.QtWidgets import QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton
from PyQt6.QtCore import Qt

class SettingsPanel:
    """Provides settings widgets to insert into a parent layout."""

    def __init__(self, parent_layout):
        self.layout = parent_layout

    def add_settings_widgets(self):
        self.username_label = QLabel("User Name:")
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        self.notifications_checkbox = QCheckBox("Enable Notifications")
        self.layout.addWidget(self.notifications_checkbox)

        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_combo)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def save_settings(self):
        username = self.username_input.text()
        notifications = self.notifications_checkbox.isChecked()
        theme = self.theme_combo.currentText()
        print(f"Settings Saved → Username: {username}, Notifications: {notifications}, Theme: {theme}")
