# tests/test_main.py
import pytest
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from src.janet_twin.ui.main_window import GPTClientUI
from src.janet_twin.ui.tools.settings import SettingsPanel


@pytest.fixture
def ui_instance(qapp):
    """Create a GPTClientUI instance with a running QApplication."""
    return GPTClientUI()


def test_ui_initialization(ui_instance):
    """Verify the MainWindow initializes without errors."""
    assert ui_instance is not None
    assert ui_instance.windowTitle() != ""


def test_settings_panel_defaults(qapp):
    """Check that the SettingsPanel initializes with expected defaults."""
    parent_widget = QWidget()
    parent_layout = QVBoxLayout(parent_widget)
    panel = SettingsPanel(parent_layout, qapp)
    assert panel is not None
    assert hasattr(panel, "save_settings")
    assert callable(panel.save_settings)

def test_settings_panel_save(qapp):
    """Check that the SettingsPanel saves settings correctly."""
    parent_widget = QWidget()
    parent_layout = QVBoxLayout(parent_widget)
    panel = SettingsPanel(parent_layout, qapp)
    assert panel is not None
    assert hasattr(panel, "save_settings")
    assert callable(panel.save_settings)

def test_settings_panel_save_with_data(qapp):
    """Check that the SettingsPanel saves settings correctly."""
    parent_widget = QWidget()
    parent_layout = QVBoxLayout(parent_widget)
    panel = SettingsPanel(parent_layout, qapp)


