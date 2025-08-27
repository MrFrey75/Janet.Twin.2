import logging
import os
from logging.handlers import RotatingFileHandler


log_dir = os.path.join(os.path.dirname(__file__), 'logs')
log_file_path = os.path.join(log_dir, 'event.log')

# Create a logger
logger = logging.getLogger("JanetTwin")
logger.setLevel(logging.DEBUG)

# Create a console handler for output to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Adjust as needed

# Create a file handler for logging to a file with rotation
# Use a relative path to avoid permission issues
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