import sys
import qdarkstyle


from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # Import tabs AFTER QApplication exists
    from gui.music_tab import MusicTab
    from gui.video_tab import VideoTab
    try:
        from gui.settings_tab import SettingsTab
        settings_exists = True
    except ImportError:
        settings_exists = False

    # Create main window
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Project Seadog")
    window.resize(800, 600)

    # Create tab widget
    tabs = QtWidgets.QTabWidget()
    window.setCentralWidget(tabs)

    # Instantiate tabs
    music_tab = MusicTab()
    video_tab = VideoTab()
    tabs.addTab(music_tab, "Music")
    tabs.addTab(video_tab, "Video")

    if settings_exists:
        settings_tab = SettingsTab()
        tabs.addTab(settings_tab, "Settings")

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
