from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
import sys
from src.app_logic.logger import logger
from src.app_logic.config import config
from src.app_logic.qrcode_logic import QRCodeManager
from src.app_ui.ui_update_window import UpdateWindow
from src.app_logic.update_logic import check_for_updates, is_version_discontinued


def show_update_window(release_data, update_file_url, versions):
    """Displays the update dialog with version details."""
    update_dialog = UpdateWindow(release_data, update_file_url, versions)
    update_dialog.exec()


def load_qss(obj: QApplication, file_path: str):
    """Loads and applies a QSS stylesheet to the application."""
    log = logger
    try:
        with open(file_path, "r") as f:
            qss = f.read()
        obj.setStyleSheet(qss)
        log.info("QSS loaded successfully from %s", file_path)
    except Exception as e:
        log.error("Failed to load QSS from %s: %s", file_path, str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._log = logger
        check_for_updates(config, self._log, show_update_window)
        self.qrcode_manager = QRCodeManager(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(config.icon_path))

    load_qss(app, config.qss_path)

    if is_version_discontinued(config):
        show_update_window(None, None, (config.app_version, ""))
        sys.exit(0)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
