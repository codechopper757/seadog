import sys
import os
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

APP_NAME = "SeaDog"
APP_VERSION = "0.2.0"


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

    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)


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

    # Import GUI after QApplication
    from gui.main_window import MainWindow  # noqa

    window = MainWindow()
    window.setWindowIcon(QIcon(icon_path))  # extra safety for some WMs
    window.resize(1000, 700)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
