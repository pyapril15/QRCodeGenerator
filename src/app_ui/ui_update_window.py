from PySide6.QtCore import Qt
from PySide6.QtGui import QLinearGradient, QColor, QPalette, QBrush
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QMessageBox

from src.app_logic.update_logic import UpdateManager


class UpdateWindow(QDialog):
    """
    Update window UI for managing application updates.
    Handles update notifications, download progress, and restart prompts.
    """

    def __init__(self, update_info, update_file_url, versions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Available")
        self.setFixedSize(400, 250)

        self.update_info = update_info or {}
        self.versions = versions
        self.update_manager = UpdateManager(update_file_url, self.versions[1])

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """Initialize the update window UI components."""
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#FFDEE9"))
        gradient.setColorAt(1, QColor("#B5FFFC"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        self.title_label = QLabel("Update Available", alignment=Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.version_label = QLabel(f"Current Version: {self.versions[0]}\nLatest Version: {self.versions[1]}",
                                    alignment=Qt.AlignCenter)
        self.version_label.setStyleSheet("font-size: 14px; color: #555;")

        description_text = self.update_info.get("body", "No description available.")
        self.description_label = QLabel(description_text, wordWrap=True, alignment=Qt.AlignCenter)
        self.description_label.setStyleSheet("font-size: 12px; color: #444;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            "QProgressBar { border-radius: 8px; height: 15px; background-color: #eee; }"
            "QProgressBar::chunk { background-color: #5cb85c; border-radius: 8px; }"
        )
        self.progress_bar.setValue(0)

        self.update_now_btn = QPushButton("Update Now")
        self.update_now_btn.setStyleSheet(
            "background-color: #5cb85c; color: white; font-size: 14px; padding: 6px; border-radius: 5px;")
        self.update_now_btn.clicked.connect(self.confirm_download)

        self.update_later_btn = QPushButton("Update Later")
        self.update_later_btn.setStyleSheet(
            "background-color: #d9534f; color: white; font-size: 14px; padding: 6px; border-radius: 5px;")
        self.update_later_btn.clicked.connect(self.close)

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_now_btn)
        button_layout.addWidget(self.update_later_btn)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.version_label)
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def init_signals(self):
        """Connect signals between the update manager and UI elements."""
        self.update_manager.progress_signal.connect(self.progress_bar.setValue)
        self.update_manager.status_signal.connect(self.show_status_message)
        self.update_manager.download_complete_signal.connect(self.show_download_complete)
        self.update_manager.restart_signal.connect(self.show_restart_message)

    def confirm_download(self):
        """Prompt user before starting the download."""
        reply = QMessageBox.question(
            self, "Download Update", "Click OK to start downloading.",
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok
        )
        if reply == QMessageBox.Ok:
            self.start_update()

    def start_update(self):
        """Disable buttons and start the update process."""
        self.update_now_btn.setEnabled(False)
        self.update_later_btn.setEnabled(False)
        self.update_manager.start_update()

    def show_download_complete(self):
        """Show download complete message, then prompt restart message."""
        reply = QMessageBox.information(
            self, "Update", "Download complete. Click OK to continue.",
            QMessageBox.Ok
        )
        if reply == QMessageBox.Ok:
            self.update_manager.close_application()

    def show_restart_message(self):
        """Show restart prompt and then close the application."""
        QMessageBox.information(self, "Update", "Restart the application manually.")
        self.close_application()

    def show_status_message(self, message):
        """Display status messages from the update manager."""
        QMessageBox.information(self, "Update", message)

    def close_application(self):
        """Close the update window and exit application."""
        self.close()
