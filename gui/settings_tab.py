from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from utils.config import ConfigManager

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.config = ConfigManager()

        layout = QVBoxLayout()

        # Music output directory
        layout.addWidget(QLabel("Default Music Output Directory:"))
        self.music_dir_input = QLineEdit()
        layout.addWidget(self.music_dir_input)

        # Video output directory
        layout.addWidget(QLabel("Default Video Output Directory:"))
        self.video_dir_input = QLineEdit()
        layout.addWidget(self.video_dir_input)

        # Kid3 checkbox
        self.kid3_checkbox = QCheckBox("Enable Kid3 integration")
        layout.addWidget(self.kid3_checkbox)

        # Gotify checkbox
        self.gotify_checkbox = QCheckBox("Enable Gotify notifications")
        layout.addWidget(self.gotify_checkbox)

        # Save button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # Load current config values into GUI
        self.load_settings()

    def load_settings(self):
        """Populate the GUI fields with values from config.json"""
        self.music_dir_input.setText(self.config.get("music_output_dir", ""))
        self.video_dir_input.setText(self.config.get("video_output_dir", ""))
        self.kid3_checkbox.setChecked(self.config.get("open_kid3_after_download", False))
        self.gotify_checkbox.setChecked(self.config.get("gotify_enabled", False))

    def save_settings(self):
        """Save GUI values back to config.json"""
        self.config.set("music_output_dir", self.music_dir_input.text())
        self.config.set("video_output_dir", self.video_dir_input.text())
        self.config.set("open_kid3_after_download", self.kid3_checkbox.isChecked())
        self.config.set("gotify_enabled", self.gotify_checkbox.isChecked())
