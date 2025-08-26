# toolbox.py
from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from .tools.settings import SettingsPanel
from .tools.conversation_history_tool import ConversationHistoryTool
from .tools.file_manager_tool import FileManagerTool
from .tools.log_viewer_tool import LogViewerTool
from .tools.raw_data_tool import RawDataTool


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

        tool_map = {
            "Conversation History": ConversationHistoryTool(),
            "File Manager": FileManagerTool(),
            "Log Viewer": LogViewerTool(),
            "Raw Data": RawDataTool(),
        }

        # Handle Settings separately because it requires the layout as a parameter.
        if name == "Settings":
            settings_panel = SettingsPanel(self.toolbox_layout)
            settings_panel.add_settings_widgets()
        elif name in tool_map:
            self.toolbox_layout.addWidget(tool_map[name])

        self.toolbox_dock.setVisible(True)
        self.toolbox_dock.raise_()