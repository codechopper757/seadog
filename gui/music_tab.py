from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox,
    QFileDialog, QTextEdit, QMessageBox
)
from controllers.music_controller import MusicController
from utils.config import ConfigManager
import validators  # pip install validators

class MusicTab(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigManager()
        self.controller = MusicController()
        self.current_thread = None

        layout = QVBoxLayout()

        # URL input
        layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        # Output directory
        layout.addWidget(QLabel("Output Directory:"))
        self.output_dir_btn = QPushButton()
        self.output_dir_btn.clicked.connect(self.select_directory)
        layout.addWidget(self.output_dir_btn)

        # Kid3 optional checkbox
        self.kid3_checkbox = QCheckBox("Open Kid3 after download")
        layout.addWidget(self.kid3_checkbox)

        # Download / Cancel buttons
        self.download_btn = QPushButton("Download Music")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        self.cancel_btn = QPushButton("Cancel Download")
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)
        layout.addWidget(self.cancel_btn)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

        # Initialize output directory from config
        self.output_dir_btn.setText(self.config.get("music_output_dir", ""))

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_btn.setText(dir_path)

    def log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def start_download(self):
        url = self.url_input.text().strip()
        output_dir = self.output_dir_btn.text()
        open_kid3 = self.kid3_checkbox.isChecked()

        if not url:
            self.log("Please enter a URL.")
            return

        if not validators.url(url):
            self.log("Invalid URL format.")
            return

        # Disable download button, enable cancel
        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        # Start download in background
        self.current_thread = self.controller.download_music(
            url=url,
            output_dir=output_dir,
            open_kid3=open_kid3,
            progress_callback=self.thread_log
        )

    def cancel_download(self):
        if self.controller.current_process:
            self.controller.current_process.terminate()
            self.log("Download cancelled.")
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

    def thread_log(self, message):
        self.log(message)
        # Re-enable buttons when finished
        if "finished" in message.lower() or "failed" in message.lower() or "cancelled" in message.lower():
            self.download_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
