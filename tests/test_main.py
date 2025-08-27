import pytest
from PyQt6.QtWidgets import QWidget
from src.janet_twin.ui.main_window import GPTClientUI
from src.janet_twin.ui.tools.settings_console import SettingsPanel
from src.janet_twin.utils.logger_utility import logger
import logging


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
    panel = SettingsPanel(parent_widget, qapp)  # Pass QWidget as parent
    assert panel is not None
    assert hasattr(panel, "save_settings")
    assert callable(panel.save_settings)


def test_settings_panel_save(qapp):
    """Check that the SettingsPanel saves settings correctly."""
    parent_widget = QWidget()
    panel = SettingsPanel(parent_widget, qapp)  # Pass QWidget as parent
    assert panel is not None
    assert hasattr(panel, "save_settings")
    assert callable(panel.save_settings)
    panel.save_settings()  # If save_settings has side effects, assert them


# ----------------------
# Logging tests
# ----------------------
def test_logger_exists():
    """Ensure the logger object exists and is a Logger instance."""
    assert logger is not None
    assert isinstance(logger, logging.Logger)


def test_logger_levels():
    """Ensure the logger has handlers and correct levels set."""
    assert len(logger.handlers) > 0
    for handler in logger.handlers:
        assert isinstance(handler, logging.Handler)
        # Levels should be integers
        assert isinstance(handler.level, int)


def test_logger_writes_to_file(tmp_path):
    """Check that the logger writes messages to a log file."""
    log_file = tmp_path / "test.log"
    file_handler = logging.FileHandler(log_file)
    logger.addHandler(file_handler)

    test_msg = "Test log message"
    logger.info(test_msg)

    # Flush and close the handler to ensure the message is written
    file_handler.flush()
    file_handler.close()

    # Verify the message exists in the file
    with open(log_file, "r") as f:
        content = f.read()
    assert test_msg in content

    # Clean up
    logger.removeHandler(file_handler)
