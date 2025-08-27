import logging
import os
from logging.handlers import RotatingFileHandler

# Use project root for consistent log location across all modules
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
log_dir = os.path.join(PROJECT_ROOT, 'logs')
log_file_path = os.path.join(log_dir, 'event.log')

# Add custom MESSAGE logging level
MESSAGE_LEVEL = 25  # Between INFO (20) and WARNING (30)
logging.addLevelName(MESSAGE_LEVEL, "MESSAGE")

def message(self, msg, *args, **kwargs):
    """Log a message with severity 'MESSAGE'."""
    if self.isEnabledFor(MESSAGE_LEVEL):
        self._log(MESSAGE_LEVEL, msg, args, **kwargs)

# Add the message method to the Logger class
logging.Logger.message = message

# Create a logger
logger = logging.getLogger("JanetTwin")
logger.setLevel(logging.DEBUG)

# Create a console handler for output to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Adjust as needed

# Create a file handler for logging to a file with rotation
os.makedirs(log_dir, exist_ok=True)
file_handler = RotatingFileHandler(log_file_path, maxBytes=10**6, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Define a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Convenience function for MESSAGE level logging
def log_message(msg, *args, **kwargs):
    """Convenience function to log a MESSAGE level entry."""
    logger.message(msg, *args, **kwargs)