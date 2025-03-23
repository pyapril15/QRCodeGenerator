import subprocess
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

from src import logger
from src.config import Config
from src.ui_qrcode import Ui_MainWindow


class QRCodeGenerator:
    """
    QR Code Generator class that encapsulates QR code generation logic.
    """

    def __init__(self, version=None, box_size=10, border=4, fill_color="#000000", back_color="#ffffff"):
        self._version = version
        self._box_size = box_size
        self._border = border
        self._fill_color = fill_color
        self._back_color = back_color

    def generate(self, data):
        """
        Generate a QR code with the given data.
        """
        qr = qrcode.QRCode(
            version=self._version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self._box_size,
            border=self._border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=self._fill_color, back_color=self._back_color)


class MainWindow(QMainWindow):
    """
    Main application window class.
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.config = Config()
        self.logger = logger.setup_logger()
        self.qr_generator = QRCodeGenerator(
            self.config.default_version,
            self.config.default_box_size,
            self.config.default_border_size,
            self.config.default_fill_color,
            self.config.default_back_color,
        )

        self.init_ui()
        self.check_for_updates()

    def init_ui(self):
        """
        Initialize UI components and event handlers.
        """
        self.ui.generate_qrcode.clicked.connect(self.create_qr_code)
        self.ui.save_qrcode.clicked.connect(self.save_qr_code)
        self.ui.select_fill_color.clicked.connect(self.select_fill_color)
        self.ui.select_background_color.clicked.connect(self.select_back_color)
        self.logger.info("Application UI initialized.")

    def create_qr_code(self):
        """
        Generate and display the QR code.
        """
        data = self.ui.textEdit.toPlainText()
        if not data:
            self.ui.result_qrcode.clear()
            QMessageBox.warning(self, "Warning", "Please enter data for QR code generation.")
            self.logger.warning("No data provided for QR code generation.")
            return

        try:
            qr_img = self.qr_generator.generate(data)
            qr_img = qr_img.convert("RGB")
            qr_pixmap = QPixmap.fromImage(ImageQt.ImageQt(qr_img))
            self.ui.result_qrcode.setPixmap(qr_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.logger.info("QR code generated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating QR code: {str(e)}")
            self.logger.error(f"Error generating QR code: {str(e)}")

    def save_qr_code(self):
        """
        Save the generated QR code as an image file.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "Images (*.png)")
        if file_path:
            try:
                self.ui.result_qrcode.pixmap().save(file_path, "PNG")
                self.logger.info(f"QR code saved at {file_path}.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save QR code: {str(e)}")
                self.logger.error(f"Failed to save QR code: {str(e)}")

    def select_fill_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.qr_generator._fill_color = color.name()
            self.ui.fill_color_value.setText(color.name())
            self.create_qr_code()
            self.logger.info(f"Selected fill color: {color.name()}")

    def select_back_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.qr_generator._back_color = color.name()
            self.ui.background_color_value.setText(color.name())
            self.create_qr_code()
            self.logger.info(f"Selected background color: {color.name()}")

    def check_for_updates(self):
        """
        Check for updates from GitHub Releases.
        """
        try:
            current_version = "1.0.0"
            owner = "pyapril15"
            repo = "qrcode_generator"

            url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(url)
            response.raise_for_status()
            release_data = response.json()
            latest_version = release_data["tag_name"].lstrip("v")

            if latest_version > current_version:
                self.download_and_install_update(release_data)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking for updates: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during update check: {str(e)}")

    def download_and_install_update(self, release_data):
        """
        Download and install the latest release from GitHub.
        """
        try:
            for asset in release_data["assets"]:
                if asset["name"].endswith(".exe"):
                    installer_url = asset["browser_download_url"]
                    installer_path = "QRCodeGenerator-update.exe"

                    response = requests.get(installer_url)
                    response.raise_for_status()

                    with open(installer_path, "wb") as f:
                        f.write(response.content)

                    subprocess.Popen([installer_path])
                    QApplication.quit()
                    return

            QMessageBox.critical(self, "Error", "Installer not found in release.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error downloading update: {str(e)}")
            self.logger.error(f"Error downloading update: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error during update: {str(e)}")
            self.logger.error(f"Unexpected error during update: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("qrcode_icon.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
