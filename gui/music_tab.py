from PyQt5 import QtWidgets, QtCore
from controllers.music_controller import MusicController
from utils.config import ConfigManager
import os

class MusicTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Controller & config
        self.controller = MusicController()
        self.config = ConfigManager()

        # Layout
        layout = QtWidgets.QVBoxLayout(self)

        # URL input
        self.url_input = QtWidgets.QLineEdit(self)
        self.url_input.setPlaceholderText("Enter YouTube URL or playlist")
        layout.addWidget(QtWidgets.QLabel("URL:"))
        layout.addWidget(self.url_input)

        # Output directory
        self.dir_input = QtWidgets.QLineEdit(self)
        self.dir_input.setPlaceholderText("Select output directory")
        self.dir_input.setText(self.config.get("music_output_dir", os.path.expanduser("~/Music")))
        layout.addWidget(QtWidgets.QLabel("Output Directory:"))
        layout.addWidget(self.dir_input)

        self.dir_button = QtWidgets.QPushButton("Browse...")
        self.dir_button.clicked.connect(self.browse_directory)
        layout.addWidget(self.dir_button)

        # Kid3 checkbox
        self.kid3_checkbox = QtWidgets.QCheckBox("Open Kid3 after download")
        self.kid3_checkbox.setChecked(True)
        layout.addWidget(self.kid3_checkbox)

        # Start / Cancel buttons
        self.start_button = QtWidgets.QPushButton("Start Download")
        self.start_button.clicked.connect(self.start_download)
        self.cancel_button = QtWidgets.QPushButton("Cancel Download")
        self.cancel_button.clicked.connect(self.cancel_download)
        layout.addWidget(self.start_button)
        layout.addWidget(self.cancel_button)

        # Status output
        self.status_output = QtWidgets.QTextEdit()
        self.status_output.setReadOnly(True)
        layout.addWidget(QtWidgets.QLabel("Status:"))
        layout.addWidget(self.status_output)

        self.setLayout(layout)

    # -----------------
    # Callbacks / slots
    # -----------------
    def browse_directory(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.dir_input.setText(dir_path)

    def start_download(self):
        url = self.url_input.text().strip()
        out_dir = self.dir_input.text().strip()
        open_kid3 = self.kid3_checkbox.isChecked()

        if not url:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a URL.")
            return

        # Disable start button to prevent multiple downloads
        self.start_button.setEnabled(False)
        self.status_output.clear()
        self.append_status(f"Starting download: {url}")

        # Start threaded download
        self.controller.start_download(
            url=url,
            output_dir=out_dir,
            open_kid3=open_kid3,
            progress_callback=self.append_status,
            finished_callback=self.download_finished
        )

    def cancel_download(self):
        self.controller.cancel_download()
        self.append_status("Download cancelled by user.")
        self.start_button.setEnabled(True)

    def append_status(self, msg):
        # Thread-safe appending
        QtCore.QMetaObject.invokeMethod(
            self.status_output,
            "append",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, msg)
        )

    def download_finished(self, success):
        if success:
            self.append_status("Download completed successfully!")
        else:
            self.append_status("Download finished with errors or cancelled.")
        self.start_button.setEnabled(True)
