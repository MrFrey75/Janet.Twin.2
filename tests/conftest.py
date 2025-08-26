# tests/conftest.py
import pytest
import sys
from PyQt6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """
    Ensure a single QApplication instance exists for the whole test session.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app
