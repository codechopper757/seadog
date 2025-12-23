from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFileDialog, QMessageBox,
    QGroupBox, QSpinBox
)
from utils.config import ConfigManager
import os
import requests


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.config = ConfigManager()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # =========================
        # Download Paths
        # =========================
        paths_group = QGroupBox("Download Paths")
        paths_layout = QVBoxLayout()

        # Music directory
        self.music_dir_input = QLineEdit()
        music_btn = QPushButton("Browse")
        music_btn.clicked.connect(lambda: self.browse_dir(self.music_dir_input))

        music_row = QHBoxLayout()
        music_row.addWidget(QLabel("Music:"))
        music_row.addWidget(self.music_dir_input)
        music_row.addWidget(music_btn)
        paths_layout.addLayout(music_row)

        # Video directory
        self.video_dir_input = QLineEdit()
        video_btn = QPushButton("Browse")
        video_btn.clicked.connect(lambda: self.browse_dir(self.video_dir_input))

        video_row = QHBoxLayout()
        video_row.addWidget(QLabel("Video:"))
        video_row.addWidget(self.video_dir_input)
        video_row.addWidget(video_btn)
        paths_layout.addLayout(video_row)

        paths_group.setLayout(paths_layout)
        main_layout.addWidget(paths_group)

        # =========================
        # Behavior
        # =========================
        behavior_group = QGroupBox("Behavior")
        behavior_layout = QVBoxLayout()

        self.kid3_checkbox = QCheckBox("Open Kid3 after music downloads")
        behavior_layout.addWidget(self.kid3_checkbox)

        delay_row = QHBoxLayout()
        self.playlist_delay_spinbox = QSpinBox()
        self.playlist_delay_spinbox.setRange(0, 600)
        self.playlist_delay_spinbox.setSuffix(" seconds")
        self.playlist_delay_spinbox.setToolTip(
            "Delay between playlist items to reduce rate limiting"
        )
        delay_row.addWidget(QLabel("Playlist delay:"))
        delay_row.addWidget(self.playlist_delay_spinbox)
        behavior_layout.addLayout(delay_row)

        behavior_group.setLayout(behavior_layout)
        main_layout.addWidget(behavior_group)

        # =========================
        # Gotify Notifications
        # =========================
        gotify_group = QGroupBox("Gotify Notifications")
        gotify_layout = QVBoxLayout()

        self.gotify_enabled_checkbox = QCheckBox("Enable Gotify notifications")
        self.gotify_enabled_checkbox.stateChanged.connect(self.toggle_gotify_fields)
        gotify_layout.addWidget(self.gotify_enabled_checkbox)

        gotify_layout.addWidget(QLabel("Gotify Server URL:"))
        self.gotify_url_input = QLineEdit()
        self.gotify_url_input.setPlaceholderText("https://gotify.example.com")
        gotify_layout.addWidget(self.gotify_url_input)

        gotify_layout.addWidget(QLabel("Gotify API Token:"))
        self.gotify_token_input = QLineEdit()
        self.gotify_token_input.setPlaceholderText("API token")
        self.gotify_token_input.setEchoMode(QLineEdit.Password)
        gotify_layout.addWidget(self.gotify_token_input)

        self.test_gotify_btn = QPushButton("Send Test Notification")
        self.test_gotify_btn.clicked.connect(self.test_gotify)
        gotify_layout.addWidget(self.test_gotify_btn)

        gotify_group.setLayout(gotify_layout)
        main_layout.addWidget(gotify_group)

        # =========================
        # Config path display
        # =========================
        config_path = os.path.join(self.config.config_dir, "config.json")
        config_path_label = QLabel(f"Config file: {config_path}")
        config_path_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(config_path_label)

        # =========================
        # Save Button
        # =========================
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(self.save_btn)

        main_layout.addStretch()
        self.setLayout(main_layout)

        self.load_settings()

    def browse_dir(self, line_edit):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            line_edit.setText(path)

    def toggle_gotify_fields(self):
        enabled = self.gotify_enabled_checkbox.isChecked()
        self.gotify_url_input.setEnabled(enabled)
        self.gotify_token_input.setEnabled(enabled)
        self.test_gotify_btn.setEnabled(enabled)

    def load_settings(self):
        self.music_dir_input.setText(
            self.config.get("music_output_dir", os.path.expanduser("~/Music"))
        )
        self.video_dir_input.setText(
            self.config.get("video_output_dir", os.path.expanduser("~/Videos"))
        )
        self.kid3_checkbox.setChecked(
            self.config.get("open_kid3_after_download", False)
        )
        self.playlist_delay_spinbox.setValue(
            self.config.get("playlist_delay", 0)
        )

        gotify_enabled = self.config.get("gotify_enabled", False)
        self.gotify_enabled_checkbox.setChecked(gotify_enabled)
        self.gotify_url_input.setText(self.config.get("gotify_url", ""))
        self.gotify_token_input.setText(self.config.get("gotify_token", ""))

        self.toggle_gotify_fields()

    def save_settings(self):
        self.config.set("music_output_dir", self.music_dir_input.text())
        self.config.set("video_output_dir", self.video_dir_input.text())
        self.config.set("open_kid3_after_download", self.kid3_checkbox.isChecked())
        self.config.set("playlist_delay", self.playlist_delay_spinbox.value())

        self.config.set("gotify_enabled", self.gotify_enabled_checkbox.isChecked())
        self.config.set("gotify_url", self.gotify_url_input.text())
        self.config.set("gotify_token", self.gotify_token_input.text())

        QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully.")

    def test_gotify(self):
        if not self.gotify_enabled_checkbox.isChecked():
            QMessageBox.warning(self, "Gotify Disabled", "Enable Gotify notifications before testing.")
            return

        url = self.gotify_url_input.text().strip()
        token = self.gotify_token_input.text().strip()

        if not url or not token:
            QMessageBox.warning(self, "Missing Information", "Please enter both Gotify URL and API token.")
            return

        try:
            r = requests.post(
                f"{url.rstrip('/')}/message?token={token}",
                json={
                    "title": "SeaDog Test Notification",
                    "message": "This is a test notification from SeaDog.",
                    "priority": 5
                },
                timeout=5
            )

            if r.status_code == 200:
                QMessageBox.information(self, "Success", "Test notification sent successfully.")
            else:
                QMessageBox.critical(
                    self,
                    "Gotify Error",
                    f"Failed to send notification.\nStatus code: {r.status_code}\nResponse: {r.text}"
                )

        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"An error occurred:\n{e}")
