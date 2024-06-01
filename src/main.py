import sys
import qrcode
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QColorDialog
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from PIL import ImageQt
from config import config
from logger import logger
from ui_qrcode import Ui_MainWindow


def load_qss(obj, file_path):
    """
    Load and apply QSS stylesheet to the given object.

    Args:
        obj: Object to apply the stylesheet to.
        file_path (str): Path to the QSS stylesheet file.
    """
    try:
        with open(file_path, "r") as f:
            qss = f.read()
        obj.setStyleSheet(qss)
        logger.info("QSS loaded successfully from %s", file_path)
    except Exception as e:
        logger.error("Failed to load QSS from %s: %s", file_path, str(e))


class MainWindow(QMainWindow):
    """
    Main window class for the QR code generator application.
    """

    def __init__(self):
        """
        Initialize the MainWindow class.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Assign UI elements to instance variables
        self.input_content = self.ui.textEdit
        self.version = self.ui.version_slider
        self.box_size = self.ui.box_size_slider
        self.border_size = self.ui.border_size_slider
        self.fill_color_btn = self.ui.select_fill_color
        self.fill_color_text = self.ui.fill_color_value
        self.back_color_btn = self.ui.select_background_color
        self.back_color_text = self.ui.background_color_value
        self.qr_code = self.ui.result_qrcode
        self.generate_btn = self.ui.generate_qrcode
        self.save_btn = self.ui.save_qrcode

        # Set default values from config
        self.version.setValue(config.default_version)
        self.box_size.setValue(config.default_box_size)
        self.border_size.setValue(config.default_border_size)
        self.fill_color_text.setText(config.default_fill_color)
        self.back_color_text.setText(config.default_back_color)

        # Clear the QR code display
        self.qr_code.clear()

        # Connect the resize event to a custom slot
        self.resizeEvent = self.on_resize

        # Connect signals to slots
        self.generate_btn.clicked.connect(self.create_qr_code)
        self.save_btn.clicked.connect(self.save_qr_code)
        self.version.valueChanged.connect(self.create_qr_code)
        self.box_size.valueChanged.connect(self.create_qr_code)
        self.border_size.valueChanged.connect(self.create_qr_code)
        self.fill_color_btn.clicked.connect(self.select_fill_color)
        self.back_color_btn.clicked.connect(self.select_back_color)

        logger.info("Main window initialized with default settings")

    def on_resize(self, event):
        """
        Handle window resize event to regenerate QR code.

        Args:
            event: Resize event.
        """
        try:
            self.create_qr_code()
            logger.info("Window resized, QR code regenerated")
        except Exception as e:
            logger.error("Error during window resize: %s", str(e))
        super(MainWindow, self).resizeEvent(event)

    def select_fill_color(self):
        """
        Slot to handle fill color selection.
        """
        fill_color = QColorDialog.getColor()
        if fill_color.isValid():
            self.fill_color_text.setText(fill_color.name())
            logger.info("Selected fill color: %s", fill_color.name())
            self.create_qr_code()

    def select_back_color(self):
        """
        Slot to handle background color selection.
        """
        back_color = QColorDialog.getColor()
        if back_color.isValid():
            self.back_color_text.setText(back_color.name())
            logger.info("Selected background color: %s", back_color.name())
            self.create_qr_code()

    def save_qr_code(self):
        """
        Slot to handle saving QR code image.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "Images (*.png)", options=options)
        if file_path:
            try:
                self.qr_code.pixmap().save(file_path, "PNG")
                logger.info("QR code saved successfully at %s", file_path)
            except Exception as e:
                logger.error("Failed to save QR code: %s", str(e))

    def create_qr_code(self):
        """
        Generate QR code based on user input.
        """
        data = self.input_content.toPlainText()
        if not data:
            self.qr_code.clear()
            logger.warning("No data provided for QR code generation")
            return

        version = self.version.value()
        if version == 0:
            version = None

        box_size = self.box_size.value()
        border = self.border_size.value()
        fill_color = self.fill_color_text.text() or config.default_fill_color
        back_color = self.back_color_text.text() or config.default_back_color

        try:
            qr = qrcode.QRCode(
                version=version,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)

            qr_img_qt = ImageQt.ImageQt(qr_img)
            qr_img_pixmap = QPixmap.fromImage(qr_img_qt)
            scaled_pixmap = qr_img_pixmap.scaled(self.qr_code.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.qr_code.setPixmap(scaled_pixmap)
            logger.info("QR code generated successfully with data: %s", data)
        except Exception as e:
            self.qr_code.clear()
            logger.error("Error generating QR code: %s", str(e))


def log_application_close():
    """
    Log application closure event.
    """
    logger.info("Application closed")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(log_application_close)  # Connect application close event to log function
    load_qss(app, config.qss_path)
    app.setWindowIcon(QIcon(config.icon_path))
    window = MainWindow()
    window.show()
    logger.info("Application started")

    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error("Error during application execution: %s", str(e))
