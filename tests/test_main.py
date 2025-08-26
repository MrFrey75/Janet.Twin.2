import pytest

# Import after sys.path is set
from src.janet_twin.ui.main_window import GPTClientUI  # <-- adjust if the class is actually in app.py

@pytest.fixture
def ui_instance():
    """Fixture to create a GPTClientUI instance for testing."""
    return GPTClientUI()

def test_ui_initialization(ui_instance):
    """Ensure the main UI class initializes correctly."""
    ui = ui_instance
    assert ui is not None
    assert hasattr(ui, 'settings_panel'), "UI should have a settings panel"

def test_settings_panel_defaults(ui_instance):
    """Check default values in the settings panel."""
    defaults = ui_instance.settings_panel.get_defaults()  # adjust if needed
    assert defaults is not None
    assert 'theme' in defaults
    assert 'assistant_name' in defaults

def test_plugin_loading(ui_instance):
    """Ensure plugins/skills are loaded correctly."""
    loaded_plugins = ui_instance.load_plugins()  # adjust if needed
    assert isinstance(loaded_plugins, list)
