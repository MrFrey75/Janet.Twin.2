# file_manager_tool.py
import os
import shutil
import uuid
import yaml
from datetime import datetime
from PyQt6.QtWidgets import (
    QLabel,
    QListWidget,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from src.janet_twin.utils.logger_utility import logger


UPLOAD_DIR = os.path.join("src", "janet_twin", "uploads")
METADATA_FILE = os.path.join("data", "struct", "file.yaml")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)

# Ensure metadata file exists
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        yaml.safe_dump([], f)


class FileManagerTool(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title label
        label = QLabel("Files Uploaded")
        self.layout.addWidget(label)

        # File list
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        # Upload button
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        # Load previously uploaded files
        self.load_uploaded_files()

    def load_uploaded_files(self):
        """Populate the list from metadata file."""
        try:
            with open(METADATA_FILE, "r") as f:
                files = yaml.safe_load(f) or []
            if isinstance(files, dict):
                files = list(files.values())
            for file_entry in files:
                self.file_list.addItem(file_entry.get("original_name", "Unknown"))
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")

    def upload_file(self):
        """Open a file dialog, copy selected files to UPLOAD_DIR, and save metadata."""
        files, _ = QFileDialog.getOpenFileNames(self, "Select File(s)")
        if not files:
            return

        # Load metadata safely
        try:
            with open(METADATA_FILE, "r") as f:
                metadata = yaml.safe_load(f) or []
            if isinstance(metadata, dict):
                metadata = list(metadata.values())
            elif not isinstance(metadata, list):
                metadata = []
        except Exception:
            metadata = []

        for file_path in files:
            original_name = os.path.basename(file_path)
            ext = os.path.splitext(file_path)[1]
            guid_filename = f"{uuid.uuid4().hex}{ext}"  # randomized filename with original extension
            stored_path = os.path.join(UPLOAD_DIR, guid_filename)

            # Copy file
            shutil.copy(file_path, stored_path)

            # Add metadata
            metadata.append({
                "original_name": original_name,
                "stored_name": guid_filename,
                "stored_path": stored_path,
                "uploaded_at": datetime.now().isoformat()
            })

            # Display the original filename in the list
            self.file_list.addItem(original_name)

            # check if file uploaded correctly
            if os.path.exists(stored_path):
                logger.info(f"File uploaded successfully: {stored_path}")
            else:
                logger.error(f"File upload failed: {stored_path}")

        # Save updated metadata back to YAML
        try:
            with open(METADATA_FILE, "w") as f:
                yaml.safe_dump(metadata, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
