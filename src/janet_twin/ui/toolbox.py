from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QApplication
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

        # Store a single instance of SettingsPanel
        self.settings_panel = None

    def show_toolbox(self, name):
        self.toolbox_dock.setWindowTitle(name)

        # Clear previous widgets except the Settings panel instance
        for i in reversed(range(self.toolbox_layout.count())):
            item = self.toolbox_layout.itemAt(i)
            if item.widget() and item.widget() is not self.settings_panel:
                item.widget().setParent(None)
            elif not item.widget():
                self.toolbox_layout.removeItem(item)

        tool_map = {
            "Conversation History": ConversationHistoryTool(),
            "File Manager": FileManagerTool(),
            "Log Viewer": LogViewerTool(),
            "Raw Data": RawDataTool(),
        }

        if name == "Settings":
            app = QApplication.instance()
            if self.settings_panel is None:
                # Create the panel once and reuse it
                self.settings_panel = SettingsPanel(self.toolbox_layout, app)
                self.settings_panel.add_settings_widgets()
            else:
                # Re-add existing panel to layout
                self.toolbox_layout.addWidget(self.settings_panel)
        elif name in tool_map:
            self.toolbox_layout.addWidget(tool_map[name])

        self.toolbox_dock.setVisible(True)
        self.toolbox_dock.raise_()
