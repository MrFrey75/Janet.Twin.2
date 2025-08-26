import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QLabel,
    QMenu,
    QMessageBox, QDialog, QLineEdit, QCheckBox, QComboBox, QPushButton,
)
from PyQt6.QtGui import QAction

# Place this near the top of app.py, after imports but before GPTClientUI
class SettingsDialog(QDialog):
    """
    A dialog window for application settings.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(400, 300)

        self.layout = QVBoxLayout(self)

        # Example setting: User Name
        self.username_label = QLabel("User Name:")
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        # Example setting: Enable Notifications
        self.notifications_checkbox = QCheckBox("Enable Notifications")
        self.layout.addWidget(self.notifications_checkbox)

        # Example setting: Theme selection
        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_combo)

        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def save_settings(self):
        username = self.username_input.text()
        notifications = self.notifications_checkbox.isChecked()
        theme = self.theme_combo.currentText()

        QMessageBox.information(
            self,
            "Settings Saved",
            f"Username: {username}\nNotifications: {notifications}\nTheme: {theme}"
        )
        self.close()


class GPTClientUI(QMainWindow):
    """
    The main application window for the GPT client UI.
    This class sets up the core layout with a top toolbar and a main chat area.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Conversational GPT Client")
        self.setGeometry(100, 100, 1200, 800)

        # --- Create a top toolbar ribbon ---
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; }")

        # --- New Chat action ---
        self.new_chat_action = QAction("New Chat", self)
        self.toolbar.addAction(self.new_chat_action)

        self.toolbar.addSeparator()

        # --- Tools actions ---
        self.tool1_action = QAction("Tool 1", self)
        self.tool2_action = QAction("Tool 2", self)
        self.tool3_action = QAction("Tool 3", self)
        self.tool4_action = QAction("Tool 4", self)

        self.toolbar.addAction(self.tool1_action)
        self.toolbar.addAction(self.tool2_action)
        self.toolbar.addAction(self.tool3_action)
        self.toolbar.addAction(self.tool4_action)

        # Connect tools to a menu
        self.tool_actions = [self.tool1_action, self.tool2_action, self.tool3_action, self.tool4_action]
        for action in self.tool_actions:
            action.triggered.connect(lambda checked, a=action: self.show_tool_popup(a.text()))

        self.toolbar.addSeparator()

        # --- Settings action ---
        self.settings_action = QAction("Settings", self)
        self.toolbar.addAction(self.settings_action)
        self.settings_action.triggered.connect(self.show_settings_menu)

        # --- Main chat area ---
        self.main_area = QWidget()
        self.main_area_layout = QVBoxLayout(self.main_area)
        self.main_area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        chat_label = QLabel("Main Chat Area (Placeholder)")
        chat_label.setStyleSheet("font-size: 24px; color: #888;")
        self.main_area_layout.addWidget(chat_label)

        self.setCentralWidget(self.main_area)

    # --- Tool popup ---
    def show_tool_popup(self, tool_name):
        QMessageBox.information(self, "Tool Clicked", f"You clicked: {tool_name}")

    # --- Settings menu ---
    def show_settings_menu(self):
        # Open the settings dialog
        dialog = SettingsDialog(self)
        dialog.exec()

    def menu_action(self, name):
        QMessageBox.information(self, "Settings Action", f"You selected: {name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPTClientUI()
    window.show()
    sys.exit(app.exec())
