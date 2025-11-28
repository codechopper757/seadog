from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog

class MusicTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # URL input
        layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        # Output directory
        layout.addWidget(QLabel("Output Directory:"))
        self.output_dir_btn = QPushButton("Select Directory")
        self.output_dir_btn.clicked.connect(self.select_directory)
        layout.addWidget(self.output_dir_btn)

        # Kid3 optional checkbox
        self.kid3_checkbox = QCheckBox("Open Kid3 after download")
        layout.addWidget(self.kid3_checkbox)

        # Download button
        self.download_btn = QPushButton("Download Music")
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_btn.setText(dir_path)
