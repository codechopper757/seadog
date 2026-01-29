from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFileDialog, QTextEdit,
    QGroupBox, QStyle, QProgressBar, QRadioButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG
from PyQt5.QtGui import QFont, QIcon
from controllers.music_controller import MusicController
from utils.config import ConfigManager
import os


class MusicTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.controller = MusicController()
        self.config = ConfigManager()

        # Create scroll area to handle content overflow
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

        # Container widget for scroll area
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add modern styling - removed invalid CSS properties
        self.setStyleSheet("""
            QGroupBox {
                background-color: #303134;
                border: 1px solid #3c4043;
                border-radius: 12px;
                padding: 20px;
                padding-top: 30px;
                margin-top: 10px;
                font-weight: 600;
                font-size: 14px;
                color: #e8eaed;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                top: -8px;
                left: 10px;
                color: #4285f4;
                font-weight: 600;
            }
            
            QLabel {
                color: #9aa0a6;
                font-size: 13px;
                font-weight: 500;
            }
            
            QLineEdit {
                background-color: #202124;
                border: 2px solid #3c4043;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #e8eaed;
            }
            
            QLineEdit:focus {
                border: 2px solid #4285f4;
                background-color: #28292c;
            }
            
            QLineEdit:disabled {
                background-color: #28292c;
                color: #5f6368;
            }
            
            QPushButton {
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #5a9af5;
            }
            
            QPushButton:pressed {
                background-color: #3367d6;
            }
            
            QPushButton:disabled {
                background-color: #3c4043;
                color: #5f6368;
            }
            
            QPushButton#browse_btn {
                background-color: #303134;
                border: 2px solid #4285f4;
                color: #4285f4;
                min-width: 80px;
            }
            
            QPushButton#browse_btn:hover {
                background-color: #3c4043;
            }
            
            QPushButton#cancel_btn {
                background-color: #5f6368;
            }
            
            QPushButton#cancel_btn:hover {
                background-color: #f44336;
            }
            
            QCheckBox {
                color: #e8eaed;
                font-size: 13px;
                spacing: 10px;
                padding: 6px;
            }
            
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #5f6368;
                background-color: #202124;
            }
            
            QCheckBox::indicator:hover {
                border-color: #8ab4f8;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4285f4;
                border-color: #4285f4;
            }
            
            QRadioButton {
                color: #e8eaed;
                font-size: 13px;
                spacing: 10px;
                padding: 6px;
            }
            
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #5f6368;
                background-color: #202124;
            }
            
            QRadioButton::indicator:hover {
                border-color: #8ab4f8;
                background-color: #28292c;
            }
            
            QRadioButton::indicator:checked {
                border: 6px solid #4285f4;
                background-color: #4285f4;
            }
            
            QTextEdit {
                background-color: #18191a;
                border: 1px solid #3c4043;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                color: #e8eaed;
            }
            
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #3c4043;
                text-align: center;
                height: 24px;
                color: white;
                font-weight: 600;
            }
            
            QProgressBar::chunk {
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4285f4, stop:0.5 #34a853, stop:1 #fbbc04);
            }
        """)

        # =========================
        # Source Section
        # =========================
        source_group = self._create_source_section()
        main_layout.addWidget(source_group)

        # =========================
        # Output Section
        # =========================
        output_group = self._create_output_section()
        main_layout.addWidget(output_group)

        # =========================
        # Settings Row (Options + Quality side by side)
        # =========================
        settings_row = QHBoxLayout()
        settings_row.setSpacing(16)
        
        options_group = self._create_options_section()
        settings_row.addWidget(options_group, 1)
        
        quality_group = self._create_quality_section()
        settings_row.addWidget(quality_group, 1)
        
        main_layout.addLayout(settings_row)

        # =========================
        # Controls Section
        # =========================
        controls_layout = self._create_controls_section()
        main_layout.addLayout(controls_layout)

        # =========================
        # Status Section
        # =========================
        status_group = self._create_status_section()
        main_layout.addWidget(status_group)

        # Add stretch to push everything up if there's extra space
        main_layout.addStretch()

        # Set the container in the scroll area
        scroll.setWidget(container)
        
        # Set scroll area as the main layout
        tab_layout = QVBoxLayout(self)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)

    def _create_source_section(self):
        """Create the source URL input section"""
        source_group = QGroupBox("🔗 Source")
        source_layout = QVBoxLayout()
        source_layout.setSpacing(10)

        url_label = QLabel("Enter YouTube URL or Playlist:")
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.url_input.setMinimumHeight(44)

        source_layout.addWidget(url_label)
        source_layout.addWidget(self.url_input)
        source_group.setLayout(source_layout)
        
        return source_group

    def _create_output_section(self):
        """Create the output directory section"""
        output_group = QGroupBox("📁 Output Directory")
        output_layout = QVBoxLayout()
        output_layout.setSpacing(10)

        dir_row = QHBoxLayout()
        dir_row.setSpacing(12)
        
        self.dir_input = QLineEdit()
        self.dir_input.setText(
            self.config.get("music_output_dir", os.path.expanduser("~/Music"))
        )
        self.dir_input.setMinimumHeight(44)

        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("browse_btn")
        browse_btn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        browse_btn.clicked.connect(self.browse_directory)
        browse_btn.setFixedWidth(120)

        dir_row.addWidget(self.dir_input, 1)
        dir_row.addWidget(browse_btn)
        
        output_layout.addLayout(dir_row)
        output_group.setLayout(output_layout)
        
        return output_group

    def _create_options_section(self):
        """Create the options section"""
        options_group = QGroupBox("⚙️ Options")
        options_layout = QVBoxLayout()
        options_layout.setSpacing(14)

        self.kid3_checkbox = QCheckBox("Open Kid3 after download")
        self.kid3_checkbox.setChecked(True)

        self.gotify_checkbox = QCheckBox("Send Gotify notification")
        self.gotify_checkbox.setChecked(True)

        options_layout.addWidget(self.kid3_checkbox)
        options_layout.addWidget(self.gotify_checkbox)
        options_layout.addStretch()

        options_group.setLayout(options_layout)
        return options_group

    def _create_quality_section(self):
        """Create the audio quality section"""
        quality_group = QGroupBox("🎵 Audio Quality")
        quality_layout = QVBoxLayout()
        quality_layout.setSpacing(14)

        self.quality_high = QRadioButton("High (320 kbps)")
        self.quality_medium = QRadioButton("Medium (192 kbps)")
        self.quality_low = QRadioButton("Low (128 kbps)")

        self.quality_high.setChecked(True)

        quality_layout.addWidget(self.quality_high)
        quality_layout.addWidget(self.quality_medium)
        quality_layout.addWidget(self.quality_low)
        quality_layout.addStretch()

        quality_group.setLayout(quality_layout)
        return quality_group

    def _create_controls_section(self):
        """Create the control buttons section"""
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)

        self.start_btn = QPushButton("⬇ Download")
        self.start_btn.setMinimumHeight(48)
        self.start_btn.clicked.connect(self.start_download)

        self.cancel_btn = QPushButton("✕ Cancel")
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setMinimumHeight(48)
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)

        controls_layout.addWidget(self.start_btn, 2)
        controls_layout.addWidget(self.cancel_btn, 1)
        
        return controls_layout

    def _create_status_section(self):
        """Create the status/progress section"""
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(12)

        # Progress bar with label
        progress_container = QVBoxLayout()
        progress_container.setSpacing(8)
        
        self.progress_label = QLabel("Ready to download")
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimumHeight(28)
        
        progress_container.addWidget(self.progress_label)
        progress_container.addWidget(self.progress_bar)
        status_layout.addLayout(progress_container)

        # Status output
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setMinimumHeight(180)
        status_layout.addWidget(self.status_output)

        status_group.setLayout(status_layout)
        return status_group

    # =========================
    # Helpers
    # =========================
    def get_audio_quality(self) -> str:
        if self.quality_medium.isChecked():
            return "5"
        if self.quality_low.isChecked():
            return "9"
        return "0"  # High default

    # =========================
    # Actions
    # =========================
    def browse_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select Music Directory")
        if path:
            self.dir_input.setText(path)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.append_status("❌ Please enter a URL.")
            self.progress_label.setText("Error: No URL provided")
            return

        self.progress_bar.setValue(0)
        self.progress_label.setText("Initializing download...")
        self.status_output.clear()
        self.toggle_controls(False)

        self.controller.start_download(
            url=url,
            output_dir=self.dir_input.text(),
            open_kid3=self.kid3_checkbox.isChecked(),
            audio_quality=self.get_audio_quality(),
            progress_callback=self.append_status,
            finished_callback=self.download_finished
        )

    def cancel_download(self):
        self.controller.cancel_download()
        self.append_status("⚠️ Download cancelled by user.")
        self.progress_label.setText("Cancelled")
        self.toggle_controls(True)

    # =========================
    # Thread-safe UI helpers
    # =========================
    def append_status(self, msg):
        QMetaObject.invokeMethod(
            self.status_output,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, msg)
        )
        
        # Update progress label if it's a progress message
        if "%" in msg or "Downloading" in msg:
            QMetaObject.invokeMethod(
                self.progress_label,
                "setText",
                Qt.QueuedConnection,
                Q_ARG(str, "Downloading...")
            )

    def download_finished(self, success):
        self.progress_bar.setValue(100 if success else 0)
        
        if success:
            self.append_status("✅ Download completed successfully!")
            self.progress_label.setText("✅ Completed")
        else:
            self.append_status("❌ Download finished with errors.")
            self.progress_label.setText("❌ Failed")
            
        self.toggle_controls(True)

    def toggle_controls(self, enabled):
        self.start_btn.setEnabled(enabled)
        self.cancel_btn.setEnabled(not enabled)
        self.url_input.setEnabled(enabled)
        self.dir_input.setEnabled(enabled)
        
        if enabled:
            self.start_btn.setText("⬇ Download")
        else:
            self.start_btn.setText("⏳ Downloading...")