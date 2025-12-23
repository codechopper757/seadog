from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.music_tab import MusicTab
from gui.video_tab import VideoTab
from gui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project SeaDog")

        tabs = QTabWidget()
        tabs.addTab(MusicTab(), "Music")
        tabs.addTab(VideoTab(), "Video")
        tabs.addTab(SettingsTab(), "Settings")

        self.setCentralWidget(tabs)

