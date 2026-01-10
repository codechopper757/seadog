from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFileDialog, QMessageBox,
    QGroupBox, QSpinBox
)
from utils.config import ConfigManager
import os


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
        music_browse_btn = QPushButton("Browse")
        music_browse_btn.clicked.connect(
            lambda: self.browse_dir(self.music_dir_input)
        )

        music_row = QHBoxLayout()
        music_row.addWidget(QLabel("Music:"))
        music_row.addWidget(self.music_dir_input)
        music_row.addWidget(music_browse_btn)
        paths_layout.addLayout(music_row)

        # Video directory
        self.video_dir_input = QLineEdit()
        video_browse_btn = QPushButton("Browse")
        video_browse_btn.clicked.connect(
            lambda: self.browse_dir(self.video_dir_input)
        )

        video_row = QHBoxLayout()
        video_row.addWidget(QLabel("Video:"))
        video_row.addWidget(self.video_dir_input)
        video_row.addWidget(video_browse_btn)
        paths_layout.addLayout(video_row)

        paths_group.setLayout(paths_layout)
        main_layout.addWidget(paths_group)

        # =========================
        # Playlist Behavior
        # =========================
        playlist_group = QGroupBox("Playlists")
        playlist_layout = QHBoxLayout()

        self.playlist_delay_spin = QSpinBox()
        self.playlist_delay_spin.setRange(0, 300)
        self.playlist_delay_spin.setSuffix(" sec")
        self.playlist_delay_spin.setToolTip(
            "Delay between playlist items to avoid rate limiting"
        )

        playlist_layout.addWidget(QLabel("Delay between items:"))
        playlist_layout.addWidget(self.playlist_delay_spin)
        playlist_layout.addStretch()

        playlist_group.setLayout(playlist_layout)
        main_layout.addWidget(playlist_group)

        # =========================
        # Gotify Notifications
        # =========================
        gotify_group = QGroupBox("Gotify Notifications")
        gotify_layout = QVBoxLayout()

        self.gotify_enabled_checkbox = QCheckBox("Enable Gotify notifications")
        self.gotify_enabled_checkbox.stateChanged.connect(
            self.toggle_gotify_fields
        )
        gotify_layout.addWidget(self.gotify_enabled_checkbox)

        self.gotify_url_input = QLineEdit()
        self.gotify_url_input.setPlaceholderText(
            "https://gotify.example.com"
        )
        gotify_layout.addWidget(QLabel("Gotify Server URL:"))
        gotify_layout.addWidget(self.gotify_url_input)

        self.gotify_token_input = QLineEdit()
        self.gotify_token_input.setPlaceholderText("API token")
        self.gotify_token_input.setEchoMode(QLineEdit.Password)
        gotify_layout.addWidget(QLabel("Gotify API Token:"))
        gotify_layout.addWidget(self.gotify_token_input)

        gotify_group.setLayout(gotify_layout)
        main_layout.addWidget(gotify_group)

        # =========================
        # Save Button
        # =========================
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(self.save_btn)

        main_layout.addStretch()
        self.setLayout(main_layout)

        self.load_settings()

    # =========================
    # Helpers
    # =========================
    def browse_dir(self, line_edit):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            line_edit.setText(path)

    def toggle_gotify_fields(self):
        enabled = self.gotify_enabled_checkbox.isChecked()
        self.gotify_url_input.setEnabled(enabled)
        self.gotify_token_input.setEnabled(enabled)

    def load_settings(self):
        self.music_dir_input.setText(
            self.config.get(
                "music_output_dir",
                os.path.expanduser("~/Music")
            )
        )
        self.video_dir_input.setText(
            self.config.get(
                "video_output_dir",
                os.path.expanduser("~/Videos")
            )
        )

        self.playlist_delay_spin.setValue(
            self.config.get("playlist_delay", 0)
        )

        gotify_enabled = self.config.get("gotify_enabled", False)
        self.gotify_enabled_checkbox.setChecked(gotify_enabled)
        self.gotify_url_input.setText(
            self.config.get("gotify_url", "")
        )
        self.gotify_token_input.setText(
            self.config.get("gotify_token", "")
        )

        self.toggle_gotify_fields()

    def save_settings(self):
        self.config.set(
            "music_output_dir",
            self.music_dir_input.text()
        )
        self.config.set(
            "video_output_dir",
            self.video_dir_input.text()
        )
        self.config.set(
            "playlist_delay",
            self.playlist_delay_spin.value()
        )

        self.config.set(
            "gotify_enabled",
            self.gotify_enabled_checkbox.isChecked()
        )
        self.config.set(
            "gotify_url",
            self.gotify_url_input.text()
        )
        self.config.set(
            "gotify_token",
            self.gotify_token_input.text()
        )

        QMessageBox.information(
            self,
            "Settings Saved",
            "Your settings have been saved successfully."
        )
