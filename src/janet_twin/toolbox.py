from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel
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
            self.toolbox_layout.itemAt(i).widget().setParent(None)

        if name == "Settings":
            SettingsPanel(self.toolbox_layout).add_settings_widgets()
        else:
            for i in range(1, 6):
                label = QLabel(f"{name} Option {i}")
                self.toolbox_layout.addWidget(label)

        self.toolbox_dock.setVisible(True)
        self.toolbox_dock.raise_()
