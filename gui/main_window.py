from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QAction,
    QMessageBox,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from gui.music_tab import MusicTab
from gui.video_tab import VideoTab
from gui.settings_tab import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Version injected from main.py after construction
        self.app_version = "0.4.0"

        # -----------------
        # Menu bar
        # -----------------
        self._setup_menubar()

        # -----------------
        # Main window
        # -----------------
        self.setWindowTitle("Project SeaDog")
        
        # Add custom styling to main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #202124;
            }
            QMainWindow::separator {
                background-color: #3c4043;
                width: 1px;
                height: 1px;
            }
        """)

        # Create tab widget with modern styling
        tabs = QTabWidget()
        tabs.setDocumentMode(True)  # Makes tabs look more integrated
        tabs.setMovable(False)  # Set to True if you want draggable tabs
        
        # Add custom styling for tab widget
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #202124;
                border-radius: 8px;
                margin-top: -1px;
            }
            
            QTabBar::tab {
                background-color: transparent;
                border: none;
                padding: 12px 24px;
                margin-right: 4px;
                font-size: 14px;
                font-weight: 500;
                color: #9aa0a6;
            }
            
            QTabBar::tab:selected {
                color: #4285f4;
                background-color: #303134;
                border-bottom: 3px solid #4285f4;
            }
            
            QTabBar::tab:hover:!selected {
                color: #e8eaed;
                background-color: #28292c;
            }
            
            QTabBar::tab:first {
                margin-left: 8px;
            }
        """)

        # Add tabs with icons (if you have icons)
        tabs.addTab(MusicTab(), "🎵 Music")
        tabs.addTab(VideoTab(), "🎬 Video")
        tabs.addTab(SettingsTab(), "⚙️ Settings")

        self.setCentralWidget(tabs)
        
        # Set minimum size for better UX
        self.setMinimumSize(900, 600)

    def _setup_menubar(self):
        """Setup the menu bar with modern styling"""
        menubar = self.menuBar()
        
        # Style the menubar
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #303134;
                color: #e8eaed;
                border-bottom: 1px solid #3c4043;
                padding: 4px;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }
            
            QMenuBar::item:selected {
                background-color: #3c4043;
            }
            
            QMenu {
                background-color: #303134;
                color: #e8eaed;
                border: 1px solid #3c4043;
                border-radius: 6px;
                padding: 4px;
            }
            
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            
            QMenu::item:selected {
                background-color: #3c4043;
            }
            
            QMenu::separator {
                height: 1px;
                background-color: #3c4043;
                margin: 4px 8px;
            }
        """)

        # File menu (optional - for future features)
        file_menu = menubar.addMenu("File")
        
        # Preferences action
        preferences_action = QAction("Preferences", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(self._open_preferences)
        file_menu.addAction(preferences_action)
        
        file_menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Help menu (right-aligned)
        help_menu = menubar.addMenu("Help")
        
        # Documentation action
        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self._open_documentation)
        help_menu.addAction(docs_action)
        
        help_menu.addSeparator()

        about_action = QAction("About SeaDog", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def _open_preferences(self):
        """Open preferences (currently just switches to Settings tab)"""
        tabs = self.centralWidget()
        tabs.setCurrentIndex(2)  # Settings tab

    def _open_documentation(self):
        """Open documentation in browser"""
        from PyQt5.QtGui import QDesktopServices
        from PyQt5.QtCore import QUrl
        QDesktopServices.openUrl(QUrl("https://github.com/codechopper757/seadog"))

    def show_about_dialog(self):
        """Show enhanced about dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("About SeaDog")
        msg.setIconPixmap(self.windowIcon().pixmap(64, 64))  # Show app icon
        
        # Modern styled message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #303134;
            }
            QMessageBox QLabel {
                color: #e8eaed;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-weight: 500;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5a9af5;
            }
            QMessageBox QPushButton:pressed {
                background-color: #3367d6;
            }
        """)
        
        msg.setText(f"""
<div style='text-align: center;'>
<h2 style='color: #4285f4; margin-bottom: 8px;'>SeaDog</h2>
<p style='color: #9aa0a6; font-size: 12px; margin: 4px 0;'>Version {self.app_version}</p>
<p style='margin-top: 16px; line-height: 1.6;'>
A modern desktop GUI for downloading music and video using yt-dlp.
</p>
<p style='margin-top: 16px; color: #9aa0a6; font-size: 12px;'>
© 2025 Eric G.
</p>
</div>
""")
        
        msg.exec_()