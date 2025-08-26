import sys
import json
import os
from PyQt6.QtWidgets import QApplication
from src.janet_twin.ui.main_window import GPTClientUI


# Updated path
SETTINGS_FILE = os.path.join("data", "struct", "user_config.json")

def load_settings():
    """Load settings from JSON, return defaults if missing or corrupted."""
    default_settings = {
        "username": "",
        "notifications": True,
        "theme": "Light"
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                default_settings.update(data)
                print("Settings loaded:", default_settings)
        except Exception as e:
            print("Failed to load settings:", e)
    return default_settings

def apply_theme(app: QApplication, theme: str):
    """Apply theme to entire app based on saved settings."""
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load settings and apply theme
    settings = load_settings()
    apply_theme(app, settings.get("theme", "Light"))

    # Launch main window
    window = GPTClientUI()
    window.show()

    sys.exit(app.exec())
