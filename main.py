import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

APP_NAME = "SeaDog"
APP_VERSION = "0.4.0"


def resource_path(relative_path):
    """
    Get absolute path to resource.
    Works for development and PyInstaller.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp dir
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def apply_dark_theme(app: QApplication):
    app.setStyle("Fusion")
    
    palette = QPalette()
    
    # Modern dark theme with warmer tones
    palette.setColor(QPalette.Window, QColor(32, 33, 36))           # Slightly blue-tinted dark
    palette.setColor(QPalette.WindowText, QColor(232, 234, 237))     # Warm white
    palette.setColor(QPalette.Base, QColor(24, 25, 26))              # Darker input fields
    palette.setColor(QPalette.AlternateBase, QColor(42, 43, 46))     # Subtle alternation
    palette.setColor(QPalette.ToolTipBase, QColor(50, 51, 54))       # Dark tooltips
    palette.setColor(QPalette.ToolTipText, QColor(232, 234, 237))    # Light tooltip text
    palette.setColor(QPalette.Text, QColor(232, 234, 237))           # Main text
    palette.setColor(QPalette.Button, QColor(48, 49, 54))            # Buttons slightly lighter
    palette.setColor(QPalette.ButtonText, QColor(232, 234, 237))     # Button text
    palette.setColor(QPalette.BrightText, QColor(244, 67, 54))       # Modern red accent
    palette.setColor(QPalette.Highlight, QColor(66, 133, 244))       # Google blue
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255)) # Pure white for contrast
    
    # Add disabled state colors for better UX
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    
    app.setPalette(palette)

def apply_modern_stylesheet(app: QApplication):
    """Apply custom stylesheet for modern UI elements"""
    stylesheet = """
        QMainWindow {
            background-color: #202124;
        }
        
        QPushButton {
            background-color: #303134;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #3c4043;
        }
        
        QPushButton:pressed {
            background-color: #5f6368;
        }
        
        QPushButton:disabled {
            background-color: #28292c;
            color: #5f6368;
        }
        
        QLineEdit, QTextEdit {
            background-color: #18191a;
            border: 1px solid #3c4043;
            border-radius: 6px;
            padding: 8px;
            font-size: 13px;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #4285f4;
        }
        
        QComboBox {
            background-color: #303134;
            border: 1px solid #3c4043;
            border-radius: 6px;
            padding: 6px 10px;
            min-width: 100px;
        }
        
        QComboBox:hover {
            border: 1px solid #5f6368;
        }
        
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        
        QComboBox::down-arrow {
            image: url(none);
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #e8eaed;
            margin-right: 6px;
        }
        
        QTabWidget::pane {
            border: 1px solid #3c4043;
            border-radius: 8px;
            background-color: #202124;
            padding: 4px;
        }
        
        QTabBar::tab {
            background-color: #303134;
            border: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 10px 20px;
            margin-right: 2px;
            font-weight: 500;
        }
        
        QTabBar::tab:selected {
            background-color: #202124;
            border-bottom: 2px solid #4285f4;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #3c4043;
        }
        
        QProgressBar {
            border: none;
            border-radius: 6px;
            background-color: #3c4043;
            text-align: center;
            height: 8px;
        }
        
        QProgressBar::chunk {
            border-radius: 6px;
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4285f4, stop:1 #34a853);
        }
        
        QCheckBox {
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #5f6368;
            background-color: #202124;
        }
        
        QCheckBox::indicator:checked {
            background-color: #4285f4;
            border-color: #4285f4;
            image: url(none);
        }
        
        QCheckBox::indicator:hover {
            border-color: #8ab4f8;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #202124;
            width: 12px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background-color: #5f6368;
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #8ab4f8;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            border: none;
            background-color: #202124;
            height: 12px;
            margin: 0;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #5f6368;
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #8ab4f8;
        }
    """
    app.setStyleSheet(stylesheet)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show SeaDog version and exit"
    )
    args = parser.parse_args()

    if args.version:
        print(f"{APP_NAME} v{APP_VERSION}")
        sys.exit(0)

    # ✅ Enable proper scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # ✅ Set application icon
    icon_path = resource_path("resources/icons/icon.png")
    app.setWindowIcon(QIcon(icon_path))

    # ✅ Apply dark theme explicitly
    apply_dark_theme(app)
    apply_modern_stylesheet(app)  # Add this line

    # Import GUI after QApplication
    from gui.main_window import MainWindow  # noqa

    window = MainWindow()
    window.app_version = APP_VERSION

    window.setWindowIcon(QIcon(icon_path))  # extra safety for some WMs
    window.resize(1100, 1200)
    window.setMinimumSize(950, 700)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
