# Janet Twin: Testing

This document outlines how to test the **Janet.Twin.2** Python application using **pytest**, including the UI, tools, and plugin modules.

---

## **1. Install pytest**

Make sure your virtual environment is active:

```bash
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

Install `pytest` if not already installed:

```bash
pip install pytest
```

---

## **2. Project Structure for Tests**

```
Janet.Twin.2/
├─ src/
│  └─ janet_twin/
│      ├─ app.py
│      ├─ __main__.py
│      ├─ ui/
│      │   ├─ main_window.py
│      │   └─ tools/
│      │       └─ settings.py
├─ tests/
│  ├─ conftest.py          # sets PYTHONPATH to src/
│  ├─ test_main.py         # tests GPTClientUI
│  └─ test_skills.py       # tests skill modules
```

---

## **3. Configure Python Path for Tests**

Create `tests/conftest.py`:

```python
import sys
import os

# Add src/ to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
```

This ensures pytest can import `janet_twin`.

---

## **4. Test the Main UI**

Create `tests/test_main.py`:

```python
import pytest
from janet_twin.app import GPTClientUI  # adjust if the class lives elsewhere

@pytest.fixture
def ui_instance():
    """Create a GPTClientUI instance for testing."""
    return GPTClientUI()

def test_ui_initialization(ui_instance):
    """Ensure the main UI class initializes correctly."""
    ui = ui_instance
    assert ui is not None
    assert hasattr(ui, 'settings_panel'), "UI should have a settings panel"

def test_settings_panel_defaults(ui_instance):
    """Check default values in the settings panel."""
    defaults = ui_instance.settings_panel.get_defaults()  # adjust method if needed
    assert defaults is not None
    assert 'theme' in defaults
    assert 'assistant_name' in defaults

def test_plugin_loading(ui_instance):
    """Ensure plugins/skills are loaded correctly."""
    loaded_plugins = ui_instance.load_plugins()  # adjust method if needed
    assert isinstance(loaded_plugins, list)
```

---

## **5. Test Skill Modules**

Create `tests/test_skills.py`:

```python
import pytest
from janet_twin.ui.tools import example_skill  # replace with actual skill module

def test_example_skill_functionality():
    """Test a sample skill plugin."""
    result = example_skill.run("test input")  # replace with actual method
    assert result is not None
    assert isinstance(result, str)
```

> Make sure your skill modules have a `run()` function for testing.

---

## **6. Run Tests**

From the project root:

```bash
pytest -v tests/
```

* `-v` shows verbose output
* Tests will automatically discover files named `test_*.py`

---

## **7. Notes**

* Ensure all directories in `src/janet_twin` have `__init__.py`
* Adjust imports if classes or methods are moved
* Use `PYTHONPATH=src` if running pytest outside the package context:

```bash
PYTHONPATH=src pytest -v tests/
```

