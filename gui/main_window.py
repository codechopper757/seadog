from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from gui.music_tab import MusicTab
from gui.video_tab import VideoTab
from gui.settings_tab import SettingsTab
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Seadog")
        self.setMinimumSize(800, 600)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.music_tab = MusicTab()
        self.video_tab = VideoTab()
        self.settings_tab = SettingsTab()

        self.tabs.addTab(self.music_tab, "Music")
        self.tabs.addTab(self.video_tab, "Video")
        self.tabs.addTab(self.settings_tab, "Settings")

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
