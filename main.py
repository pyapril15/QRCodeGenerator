import sys
import qrcode
import requests
from PIL import ImageQt
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QColorDialog,
    QMessageBox,
)

from src.app_logic import logger
from src.app_logic.config import config
from src.app_ui.ui_qrcode import Ui_MainWindow
from src.app_ui.ui_update_window import UpdateWindow


class MainWindow(QMainWindow):
    """Main application window for QR code generation and management."""

    def __init__(self):
        """Initialize the main window and its components."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup logging
        self.logger = logger.setup_logger()

        # Assign UI components
        self.qr_code = self.ui.result_qrcode
        self.version_slider = self.ui.version_slider
        self.box_size_slider = self.ui.box_size_slider
        self.border_size_slider = self.ui.border_size_slider

        # Set default QR code properties
        self.current_version = config.default_version
        self.current_box_size = config.default_box_size
        self.current_border_size = config.default_border_size
        self.current_fill_color = config.default_fill_color
        self.current_back_color = config.default_back_color

        self.qr_code.clear()

        # Connect UI events
        self.init_ui()
        self.check_for_updates()

    def init_ui(self):
        """Connect UI components to their respective event handlers."""
        self.ui.generate_qrcode.clicked.connect(self.create_qr_code)
        self.ui.save_qrcode.clicked.connect(self.save_qr_code)
        self.ui.select_fill_color.clicked.connect(self.select_fill_color)
        self.ui.select_background_color.clicked.connect(self.select_back_color)

        # Connect sliders to dynamically update QR code
        self.version_slider.valueChanged.connect(self.update_version)
        self.box_size_slider.valueChanged.connect(self.update_box_size)
        self.border_size_slider.valueChanged.connect(self.update_border_size)

        self.logger.info("Application UI initialized.")

    def update_version(self):
        """Update QR code version dynamically and regenerate the QR code."""
        self.current_version = self.version_slider.value()
        self.create_qr_code()

    def update_box_size(self):
        """Update QR code box size dynamically and regenerate the QR code."""
        self.current_box_size = self.box_size_slider.value()
        self.create_qr_code()

    def update_border_size(self):
        """Update QR code border size dynamically and regenerate the QR code."""
        self.current_border_size = self.border_size_slider.value()
        self.create_qr_code()

    def create_qr_code(self):
        """Generates and displays a QR code from user input text."""
        data = self.ui.textEdit.toPlainText()

        if not data:
            self.qr_code.clear()
            QMessageBox.warning(self, "Warning", "Please enter data for QR code generation.")
            self.logger.warning("No data provided for QR code generation.")
            return

        try:
            # Create the QR code with current properties
            qr = qrcode.QRCode(
                version=self.current_version if self.current_version > 0 else None,  # Auto fit if version is 0
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.current_box_size,
                border=self.current_border_size,
            )
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=self.current_fill_color, back_color=self.current_back_color)

            # Convert QR code image to Qt format
            qr_img = qr_img.convert("RGB")
            qr_qt_img = ImageQt.ImageQt(qr_img)
            qr_pixmap = QPixmap.fromImage(qr_qt_img)

            # Scale QR code to fit QLabel while maintaining aspect ratio
            qr_pixmap = qr_pixmap.scaled(self.qr_code.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.qr_code.setPixmap(qr_pixmap)

            self.logger.info(
                f"QR code generated successfully: Version {self.current_version}, "
                f"Box Size {self.current_box_size}, Border {self.current_border_size}."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating QR code: {str(e)}")
            self.logger.error(f"Error generating QR code: {str(e)}")

    def save_qr_code(self):
        """Saves the generated QR code as an image file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "Images (*.png)")
        if file_path:
            try:
                self.qr_code.pixmap().save(file_path, "PNG")
                self.logger.info(f"QR code saved at {file_path}.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save QR code: {str(e)}")
                self.logger.error(f"Failed to save QR code: {str(e)}")

    def select_fill_color(self):
        """Allows the user to choose a fill color for the QR code."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_fill_color = color.name()
            self.ui.fill_color_value.setText(color.name())
            self.create_qr_code()
            self.logger.info(f"Selected fill color: {color.name()}")

    def select_back_color(self):
        """Allows the user to choose a background color for the QR code."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_back_color = color.name()
            self.ui.background_color_value.setText(color.name())
            self.create_qr_code()
            self.logger.info(f"Selected background color: {color.name()}")

    def check_for_updates(self):
        """Checks for application updates and prompts the user if a newer version is available."""
        try:
            current_version = config.app_version
            owner = "pyapril15"
            repo = "QRCodeGenerator"

            url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(url)
            response.raise_for_status()
            release_data = response.json()
            latest_version = release_data["tag_name"].lstrip("v")

            if latest_version > current_version:
                update_file_url = next(
                    (asset["browser_download_url"] for asset in release_data.get("assets", []) if asset["name"].endswith(".exe")),
                    None
                )

                if update_file_url:
                    update_dialog = UpdateWindow(release_data, update_file_url, (current_version, latest_version))
                    update_dialog.exec()

                    self.logger.info("Update downloaded. Closing application for manual restart.")
                    self.close()
                    QApplication.instance().quit()
                    sys.exit(0)
                else:
                    self.logger.error("No .exe update file found in the latest release.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking for updates: {str(e)}")


def load_qss(obj: QApplication, file_path: str):
    """Loads and applies a QSS stylesheet to the application."""
    log = logger.setup_logger()
    try:
        with open(file_path, "r") as f:
            qss = f.read()
        obj.setStyleSheet(qss)
        log.info("QSS loaded successfully from %s", file_path)
    except Exception as e:
        log.error("Failed to load QSS from %s: %s", file_path, str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(config.icon_path))
    load_qss(app, config.qss_path)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
