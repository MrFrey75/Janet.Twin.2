import json
import os
from PyQt6.QtWidgets import QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, QApplication

SETTINGS_FILE = os.path.join("data", "struct", "user_config.json")

class SettingsPanel:
    """Provides settings widgets to insert into a parent layout."""

    def __init__(self, parent_layout, app: QApplication):
        self.layout = parent_layout
        self.app = app  # store QApplication reference for live theme changes
        self.settings = {
            "username": "",
            "notifications": True,
            "theme": "Light"
        }
        self.load_settings()

    def add_settings_widgets(self):
        # Username
        self.username_label = QLabel("User Name:")
        self.username_input = QLineEdit(self.settings.get("username", ""))
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        # Notifications
        self.notifications_checkbox = QCheckBox("Enable Notifications")
        self.notifications_checkbox.setChecked(self.settings.get("notifications", True))
        self.layout.addWidget(self.notifications_checkbox)

        # Theme
        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Solarized", "Dracula", "Monokai", "Gruvbox"])
        current_theme = self.settings.get("theme", "Light")
        if current_theme in [self.theme_combo.itemText(i) for i in range(self.theme_combo.count())]:
            self.theme_combo.setCurrentText(current_theme)
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_combo)

        # Save Button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def load_settings(self):
        """Load settings from JSON file if it exists."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    self.settings.update(json.load(f))
                    print("Settings loaded:", self.settings)
            except Exception as e:
                print("Failed to load settings:", e)

    def save_settings(self):
        """Save current settings to JSON file and apply theme live."""
        self.settings["username"] = self.username_input.text()
        self.settings["notifications"] = self.notifications_checkbox.isChecked()
        self.settings["theme"] = self.theme_combo.currentText()

        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
            print(f"Settings Saved → {self.settings}")
        except Exception as e:
            print("Failed to save settings:", e)

        # Apply theme live
        self.apply_theme(self.app)

    def apply_theme(self, app: QApplication):
        """Apply the selected theme to the entire application."""
        theme = self.settings.get("theme", "Light")
        stylesheet = ""

        if theme == "Light":
            stylesheet = "QWidget { background-color: #ffffff; color: #000000; }"
        elif theme == "Dark":
            stylesheet = "QWidget { background-color: #2b2b2b; color: #f0f0f0; }"
        elif theme == "Solarized":
            stylesheet = "QWidget { background-color: #fdf6e3; color: #657b83; }"
        elif theme == "Dracula":
            stylesheet = "QWidget { background-color: #282a36; color: #f8f8f2; }"
        elif theme == "Monokai":
            stylesheet = "QWidget { background-color: #272822; color: #f8f8f2; }"
        elif theme == "Gruvbox":
            stylesheet = "QWidget { background-color: #282828; color: #ebdbb2; }"

        app.setStyleSheet(stylesheet)
