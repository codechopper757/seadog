from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog

class VideoTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # URL input
        layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        # Playlist checkbox
        self.playlist_checkbox = QCheckBox("This is a playlist")
        layout.addWidget(self.playlist_checkbox)

        # Output directory
        layout.addWidget(QLabel("Output Directory:"))
        self.output_dir_btn = QPushButton("Select Directory")
        self.output_dir_btn.clicked.connect(self.select_directory)
        layout.addWidget(self.output_dir_btn)

        # Download button
        self.download_btn = QPushButton("Download Video/Playlist")
        layout.addWidget(self.download_btn)

        # Playlist monitor checkbox
        self.monitor_checkbox = QCheckBox("Follow playlist and auto-download new content")
        layout.addWidget(self.monitor_checkbox)

        self.setLayout(layout)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_btn.setText(dir_path)
