from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QAction,
    QMessageBox,
    QWidget,
)
from PyQt5.QtCore import Qt

from gui.music_tab import MusicTab
from gui.video_tab import VideoTab
from gui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Version injected from main.py after construction
        self.app_version = "0.3.0"

        # -----------------
        # Menu bar
        # -----------------
        menubar = self.menuBar()

        # Spacer to push Help menu to the right
        menubar.addSeparator()
        menubar.setCornerWidget(QWidget(), Qt.TopLeftCorner)

        help_menu = menubar.addMenu("Help")

        about_action = QAction("About SeaDog", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        # -----------------
        # Main window
        # -----------------
        self.setWindowTitle("Project SeaDog")

        tabs = QTabWidget()
        tabs.addTab(MusicTab(), "Music")
        tabs.addTab(VideoTab(), "Video")
        tabs.addTab(SettingsTab(), "Settings")

        self.setCentralWidget(tabs)

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About SeaDog",
            f"""
<b>SeaDog</b><br>
Version {self.app_version}<br><br>
A simple desktop GUI for downloading music and video using yt-dlp.<br><br>
© Eric G.
"""
        )
