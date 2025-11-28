from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

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
        layout.addWidget(self.save_btn)

        self.setLayout(layout)
