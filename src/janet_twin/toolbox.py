from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit, QComboBox
from PyQt6.QtCore import Qt
from settings import SettingsPanel


class ToolboxDock:
    """Right-side dock for tools and settings."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.toolbox_dock = QDockWidget("Toolbox", main_window)
        self.toolbox_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.toolbox_dock.setFloating(False)
        self.toolbox_dock.setVisible(False)

        self.toolbox_widget = QWidget()
        self.toolbox_layout = QVBoxLayout(self.toolbox_widget)
        self.toolbox_widget.setLayout(self.toolbox_layout)
        self.toolbox_dock.setWidget(self.toolbox_widget)

        main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.toolbox_dock)

    def show_toolbox(self, name):
        self.toolbox_dock.setWindowTitle(name)

        # Clear previous widgets
        for i in reversed(range(self.toolbox_layout.count())):
            item = self.toolbox_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.toolbox_layout.removeItem(item)

        if name == "Settings":
            SettingsPanel(self.toolbox_layout).add_settings_widgets()
        elif name == "Conversation History":
            self.add_conversation_history_widgets()
        elif name == "File Manager":
            self.add_file_manager_widgets()
        elif name == "Log Viewer":
            self.add_log_viewer_widgets()
        elif name == "Raw Data":
            self.add_raw_data_widgets()

        self.toolbox_dock.setVisible(True)
        self.toolbox_dock.raise_()

    def add_conversation_history_widgets(self):
        """Adds widgets for viewing conversation history."""
        label = QLabel("Conversation History")
        self.toolbox_layout.addWidget(label)
        history_list = QListWidget()
        history_list.addItem("Chat 1: August 26, 2025")
        history_list.addItem("Chat 2: August 25, 2025")
        self.toolbox_layout.addWidget(history_list)

    def add_file_manager_widgets(self):
        """Adds widgets for managing uploaded files."""
        label = QLabel("Files Uploaded")
        self.toolbox_layout.addWidget(label)
        file_list = QListWidget()
        file_list.addItem("document.pdf")
        file_list.addItem("notes.txt")
        self.toolbox_layout.addWidget(file_list)

    def add_log_viewer_widgets(self):
        """Adds widgets for viewing log files."""
        log_label = QLabel("Select a Log File:")
        self.toolbox_layout.addWidget(log_label)
        log_selector = QComboBox()
        log_selector.addItem("app.log")
        log_selector.addItem("debug.log")
        self.toolbox_layout.addWidget(log_selector)
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setPlaceholderText("Log content will appear here...")
        self.toolbox_layout.addWidget(log_display)

    def add_raw_data_widgets(self):
        """Adds widgets for viewing raw streaming data."""
        label = QLabel("Raw Streaming Data (last 1000 lines)")
        self.toolbox_layout.addWidget(label)
        raw_data_display = QTextEdit()
        raw_data_display.setReadOnly(True)
        raw_data_display.setPlaceholderText("Raw data will stream here...")
        self.toolbox_layout.addWidget(raw_data_display)