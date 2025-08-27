import yaml

from PyQt6.QtWidgets import QDockWidget, QTabWidget, QWidget, QVBoxLayout
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

        self.tools = {
            "Conversation History": ConversationHistoryTool(),
            "File Manager": FileManagerTool(),
            "Log Viewer": LogViewerTool(),
            "Raw Data": RawDataTool(),
            "Settings": SettingsPanel(self.parent)
        }

        self.tab_widget = QTabWidget()
        for name, tool in self.tools.items():
            self.tab_widget.addTab(tool, name)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.tab_widget)
        self.setWidget(main_widget)
        self.hide()

    def show_toolbox(self, tool_name):
        """
        Shows the toolbox with a specific tab selected.
        """
        if tool_name in self.tools:
            index = self.tab_widget.indexOf(self.tools[tool_name])
            if index != -1:
                self.tab_widget.setCurrentIndex(index)
                if self.isVisible():
                    self.hide()
                else:
                    self.show()

