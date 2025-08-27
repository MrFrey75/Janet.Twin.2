import os
import yaml
from src.janet_twin.logger import logger


SETTINGS_FILE = os.path.join("data", "struct", "user_config.yaml")

class SettingsUtility:
    def __init__(self):
        self.settings = {}

    def load_settings(self):
        """Load settings from YAML file if it exists."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    loaded = yaml.safe_load(f)
                    if isinstance(loaded, dict):
                        self.settings.update(loaded)
                        logger.info("Settings loaded:", self.settings)
            except Exception as e:
                logger.error("Failed to load settings:", e)

    def expose_settings(self):
        """Expose settings to the UI."""
        return self.settings

