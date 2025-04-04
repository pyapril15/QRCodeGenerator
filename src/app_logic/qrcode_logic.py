import qrcode
from PIL import ImageQt
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QColorDialog, QMessageBox

from src.app_logic.config import config
from src.app_logic.logger import logger
from src.app_ui.ui_qrcode import Ui_MainWindow


class QRCodeManager:
    """Handles QR code generation, UI interactions, and settings management."""

    def __init__(self, parent, log=logger, _config=config):
        """Initializes the QRCodeManager with UI elements and default settings."""
        super().__init__()
        self.parent = parent
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self.parent)

        # Logger and Configuration
        self._log = log
        self._config = _config

        # UI Elements
        self._qrcode_display = self._ui.result_qrcode
        self._version_slider = self._ui.version_slider
        self._box_size_slider = self._ui.box_size_slider
        self._border_size_slider = self._ui.border_size_slider

        # QR Code Properties
        self._qr_version = self._config.qrcode_default_version
        self._qr_box_size = self._config.qrcode_default_box_size
        self._qr_border_size = self._config.qrcode_default_border_size
        self._qr_fill_color = self._config.qrcode_default_fill_color
        self._qr_bg_color = self._config.qrcode_default_bg_color

        # Clear initial QR code display
        self._qrcode_display.clear()

        # Connect UI Events
        self._init_signals()

    def _init_signals(self):
        """Connects UI components to their respective event handlers."""
        self._ui.generate_qrcode.clicked.connect(self.generate_qrcode)
        self._ui.save_qrcode.clicked.connect(self.save_qrcode)
        self._ui.select_fill_color.clicked.connect(self.select_fill_color)
        self._ui.select_background_color.clicked.connect(self.select_bg_color)

        # Sliders to dynamically update QR code
        self._version_slider.valueChanged.connect(self._update_qr_version)
        self._box_size_slider.valueChanged.connect(self._update_qr_box_size)
        self._border_size_slider.valueChanged.connect(self._update_qr_border_size)

        self._log.info("QR Code Manager initialized successfully.")

    def _update_qr_version(self):
        """Updates the QR code version and regenerates the QR code."""
        self._qr_version = self._version_slider.value()
        self.generate_qrcode()

    def _update_qr_box_size(self):
        """Updates the QR code box size and regenerates the QR code."""
        self._qr_box_size = self._box_size_slider.value()
        self.generate_qrcode()

    def _update_qr_border_size(self):
        """Updates the QR code border size and regenerates the QR code."""
        self._qr_border_size = self._border_size_slider.value()
        self.generate_qrcode()

    def generate_qrcode(self):
        """Generates and displays a QR code based on user input."""
        data = self._ui.textEdit.toPlainText().strip()

        if not data:
            self._qrcode_display.clear()
            QMessageBox.warning(self.parent, "Warning", "Please enter data for QR code generation.")
            self._log.warning("No data provided for QR code generation.")
            return

        try:
            qr = self._create_qr_code(data)
            self._display_qr_code(qr)
            self._log.info(f"QR code generated successfully: Version {self._qr_version}, "
                           f"Box Size {self._qr_box_size}, Border {self._qr_border_size}.")
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error generating QR code: {str(e)}")
            self._log.error(f"Error generating QR code: {str(e)}")

    def _create_qr_code(self, data):
        """Creates a QR code image with current settings."""
        qr = qrcode.QRCode(
            version=self._qr_version if self._qr_version > 0 else None,  # Auto-fit if 0
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self._qr_box_size,
            border=self._qr_border_size,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=self._qr_fill_color, back_color=self._qr_bg_color)

    def _display_qr_code(self, qr_img):
        """Converts the QR code image to Qt format and displays it."""
        qr_img = qr_img.convert("RGB")
        qt_img = ImageQt.ImageQt(qr_img)
        pixmap = QPixmap.fromImage(qt_img)
        scaled_pixmap = pixmap.scaled(self._qrcode_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._qrcode_display.setPixmap(scaled_pixmap)

    def save_qrcode(self):
        """Saves the generated QR code as an image file."""
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Save QR Code", "", "Images (*.png)")
        if file_path:
            try:
                self._qrcode_display.pixmap().save(file_path, "PNG")
                self._log.info(f"QR code saved successfully at {file_path}.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Failed to save QR code: {str(e)}")
                self._log.error(f"Failed to save QR code: {str(e)}")

    def select_fill_color(self):
        """Allows the user to select a fill color for the QR code."""
        color = QColorDialog.getColor()
        if color.isValid():
            self._qr_fill_color = color.name()
            self._ui.fill_color_value.setText(color.name())
            self.generate_qrcode()
            self._log.info(f"Selected fill color: {color.name()}")

    def select_bg_color(self):
        """Allows the user to select a background color for the QR code."""
        color = QColorDialog.getColor()
        if color.isValid():
            self._qr_bg_color = color.name()
            self._ui.background_color_value.setText(color.name())
            self.generate_qrcode()
            self._log.info(f"Selected background color: {color.name()}")
