import yaml

from PyQt6.QtWidgets import QDockWidget, QStackedWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from src.janet_twin.logger import logger
from .tools.conversation_history_tool import ConversationHistoryTool
from .tools.log_viewer_tool import LogViewerTool
from .tools.file_manager_tool import FileManagerTool
from .tools.raw_data_tool import RawDataTool
from .tools.settings_console import SettingsPanel


class ToolboxDock(QDockWidget):
    """
    A dockable toolbox with various developer-focused tools.
    """

    def __init__(self, parent=None):
        super().__init__("Toolbox", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)
        self.parent = parent

        # Set a reasonable fixed width for the toolbox
        self.setMinimumWidth(300)
        self.setMaximumWidth(450)

        self.tools = {
            "Conversation History": ConversationHistoryTool(),
            "File Manager": FileManagerTool(),
            "Log Viewer": LogViewerTool(),
            "Raw Data": RawDataTool(),
            "Settings": SettingsPanel(self.parent)
        }

        self.stacked_widget = QStackedWidget()
        self.tool_map = {}

        for name, tool in self.tools.items():
            self.tool_map[name] = self.stacked_widget.addWidget(tool)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.stacked_widget)
        self.setWidget(main_widget)

        # Initially hide the dock widget
        self.hide()

    def show_toolbox(self, tool_name):
        """
        Shows the toolbox with a specific tool selected and toggles visibility.
        """
        if tool_name in self.tool_map:
            # Set the current widget in the stacked widget
            self.stacked_widget.setCurrentIndex(self.tool_map[tool_name])

            # Toggle the visibility of the entire dock widget
            if self.isVisible():
                self.hide()
            else:
                self.show()