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

from src import logger  # Custom logging module
from src.config import config  # Configuration handling
from src.ui_qrcode import Ui_MainWindow  # UI class generated from .ui file


class QRCodeGenerator:
    """
    Encapsulates QR code generation logic.

    This class handles the creation of QR codes with specified parameters.
    """

    def __init__(self, version=None, box_size=10, border=4, fill_color="#000000", back_color="#ffffff"):
        """
        Initializes the QR code generator.

        Args:
            version (int, optional): QR code version (1-40). Defaults to None.
            box_size (int): Size of each box in the QR code.
            border (int): Border size around the QR code.
            fill_color (str): Fill color of the QR code (e.g., "#000000").
            back_color (str): Background color of the QR code (e.g., "#ffffff").
        """
        self._version = version
        self._box_size = box_size
        self._border = border
        self._fill_color = fill_color
        self._back_color = back_color

    def generate(self, data: str) -> ImageQt.Image:
        """
        Generates a QR code image.

        Args:
            data (str): The data to encode in the QR code.

        Returns:
            ImageQt.Image: A PIL Image object representing the generated QR code.
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
    Main application window.

    This class defines the main window of the QR code generator application,
    handling user interface interactions and QR code generation.
    """

    def __init__(self):
        """
        Initializes the main window.
        """
        super().__init__()
        self.ui = Ui_MainWindow()  # set up the UI from the generated .ui file
        self.ui.setupUi(self)

        self.logger = logger.setup_logger()  # Initialize the logger
        self.qr_generator = QRCodeGenerator(  # Initialize the QR code generator with default settings
            config.default_version,
            config.default_box_size,
            config.default_border_size,
            config.default_fill_color,
            config.default_back_color,
        )

        self.init_ui()  # Initialize UI event handlers
        self.check_for_updates()  # Check for updates on application start

    def init_ui(self):
        """
        Initializes UI components and connects event handlers.

        This method sets up the user interface by connecting the signals
        from UI elements to the corresponding methods.
        """
        self.ui.generate_qrcode.clicked.connect(self.create_qr_code)
        self.ui.save_qrcode.clicked.connect(self.save_qr_code)
        self.ui.select_fill_color.clicked.connect(self.select_fill_color)
        self.ui.select_background_color.clicked.connect(self.select_back_color)
        self.logger.info("Application UI initialized.")

    def create_qr_code(self):
        """
        Generates and displays the QR code.

        This method retrieves the data from the text edit, generates the QR code
        using the QRCodeGenerator, and displays it in the UI.
        """
        data = self.ui.textEdit.toPlainText()

        if not data:
            self.ui.result_qrcode.clear()
            QMessageBox.warning(self, "Warning", "Please enter data for QR code generation.")
            self.logger.warning("No data provided for QR code generation.")
            return

        try:
            qr_img = self.qr_generator.generate(data)
            qr_img = qr_img.convert("RGB")  # Ensure image is in RGB format
            qr_pixmap = QPixmap.fromImage(ImageQt.ImageQt(qr_img))
            self.ui.result_qrcode.setPixmap(qr_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.logger.info("QR code generated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating QR code: {str(e)}")
            self.logger.error(f"Error generating QR code: {str(e)}")

    def save_qr_code(self):
        """
        Saves the generated QR code as a PNG image file.

        This method opens a file dialog to allow the user to select a save location
        and then saves the QR code image.
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
        """
        Opens a color dialog for selecting the QR code fill color.

        This method allows the user to choose a color for the QR code's foreground.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.qr_generator._fill_color = color.name()
            self.ui.fill_color_value.setText(color.name())
            self.create_qr_code()  # Regenerate QR code with new color
            self.logger.info(f"Selected fill color: {color.name()}")

    def select_back_color(self):
        """
        Opens a color dialog for selecting the QR code background color.

        This method allows the user to choose a color for the QR code's background.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.qr_generator._back_color = color.name()
            self.ui.background_color_value.setText(color.name())
            self.create_qr_code()  # Regenerate QR code with new color
            self.logger.info(f"Selected background color: {color.name()}")

    def check_for_updates(self):
        """
        Checks for updates from GitHub Releases.

        This method uses the GitHub API to check for new releases and, if a newer
        version is available, initiates the download and installation process.
        """
        try:
            current_version = config.app_version  # Consider fetching this from a constant or file.
            owner = "pyapril15"
            repo = "QRCodeGenerator"

            url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            release_data = response.json()
            latest_version = release_data["tag_name"].lstrip("v")  # Remove potential 'v' prefix

            if latest_version > current_version:
                self.download_and_install_update(release_data)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking for updates: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during update check: {str(e)}")

    def download_and_install_update(self, release_data):
        """
        Downloads and installs the latest release from GitHub.

        This method iterates through the release assets to find an executable,
        downloads it, and then executes the installer.
        """
        try:
            for asset in release_data["assets"]:
                if asset["name"].endswith(".exe"):
                    installer_url = asset["browser_download_url"]
                    installer_path = "QRCodeGenerator-update.exe"  # Consider a more robust path

                    response = requests.get(installer_url, stream=True)  # Use stream for large files
                    response.raise_for_status()

                    with open(installer_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    subprocess.Popen([installer_path])  # Execute the installer
                    QApplication.quit()  # Close the application
                    return

            QMessageBox.critical(self, "Error", "Installer not found in release.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error downloading update: {str(e)}")
            self.logger.error(f"Error downloading update: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error during update: {str(e)}")
            self.logger.error(f"Unexpected error during update: {str(e)}")


def load_qss(obj: QApplication, file_path: str):
    """
    Loads and applies a QSS stylesheet to the given QApplication object.

    Args:
        obj (QApplication): The QApplication object to apply the stylesheet to.
        file_path (str): The path to the QSS stylesheet file.
    """
    log = logger.setup_logger()  # Get the logger
    try:
        with open(file_path, "r") as f:
            qss = f.read()
        obj.setStyleSheet(qss)
        log.info("QSS loaded successfully from %s", file_path)
    except Exception as e:
        log.error("Failed to load QSS from %s: %s", file_path, str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(config.icon_path))  # Set application icon
    load_qss(app, config.qss_path)  # Load the stylesheet
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
