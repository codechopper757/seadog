from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFileDialog, QTextEdit,
    QGroupBox, QStyle, QProgressBar
)
from PyQt5 import QtCore
from controllers.video_controller import VideoController
from utils.config import ConfigManager
import os


class VideoTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.controller = VideoController()
        self.config = ConfigManager()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # =========================
        # Source
        # =========================
        source_group = QGroupBox("Source")
        source_layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("YouTube URL or playlist")

        source_layout.addWidget(QLabel("URL:"))
        source_layout.addWidget(self.url_input)
        source_group.setLayout(source_layout)
        main_layout.addWidget(source_group)

        # =========================
        # Output
        # =========================
        output_group = QGroupBox("Output")
        output_layout = QHBoxLayout()

        self.dir_input = QLineEdit()
        self.dir_input.setText(
            self.config.get("video_output_dir", os.path.expanduser("~/Videos"))
        )

        browse_btn = QPushButton("Browse")
        browse_btn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        browse_btn.clicked.connect(self.browse_directory)

        output_layout.addWidget(self.dir_input)
        output_layout.addWidget(browse_btn)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # =========================
        # Options
        # =========================
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()

        self.gotify_checkbox = QCheckBox("Send Gotify notification on completion")
        self.gotify_checkbox.setChecked(True)

        options_layout.addWidget(self.gotify_checkbox)
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # =========================
        # Controls
        # =========================
        controls_layout = QHBoxLayout()

        self.start_btn = QPushButton("Download")
        self.start_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.start_btn.clicked.connect(self.start_download)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)

        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(controls_layout)

        # =========================
        # Status
        # =========================
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        clear_btn = QPushButton("Clear Status")
        clear_btn.clicked.connect(self.clear_status)
        status_layout.addWidget(clear_btn)


        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        status_layout.addWidget(self.progress_bar)

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        status_layout.addWidget(self.status_output)

        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        self.setLayout(main_layout)

    # =========================
    # Actions
    # =========================
    def clear_status(self):
        self.status_output.clear()
        self._set_progress(0)


    def browse_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select Video Directory")
        if path:
            self.dir_input.setText(path)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.append_status("Please enter a URL.")
            return

        self._set_progress(0)
        self.toggle_controls(False)
        self.status_output.clear()

        self.controller.start_download(
            url=url,
            output_dir=self.dir_input.text(),
            send_notification=self.gotify_checkbox.isChecked(),
            progress_callback=self.append_status,
            finished_callback=self.download_finished
        )

    def cancel_download(self):
        self.controller.cancel_download()
        self.append_status("Download cancelled.")
        self.toggle_controls(True)

    # =========================
    # Thread-safe UI helpers
    # =========================
    def append_status(self, msg):
        self.update_progress_from_line(msg)
        QtCore.QMetaObject.invokeMethod(
            self.status_output,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, msg)
        )

    def update_progress_from_line(self, line):
        if "%" in line:
            try:
                percent = int(float(line.split("%")[0].split()[-1]))
                self._set_progress(percent)
            except Exception:
                pass

    def _set_progress(self, value: int):
        QtCore.QMetaObject.invokeMethod(
            self.progress_bar,
            "setValue",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(int, value)
        )

    def download_finished(self, success):
        self._set_progress(100 if success else 0)
        self.append_status("Finished." if success else "Finished with errors.")
        self.toggle_controls(True)

    def toggle_controls(self, enabled):
        self.start_btn.setEnabled(enabled)
        self.cancel_btn.setEnabled(not enabled)
        self.url_input.setEnabled(enabled)
        self.dir_input.setEnabled(enabled)
