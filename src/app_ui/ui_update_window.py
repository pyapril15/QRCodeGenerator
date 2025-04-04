import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QLinearGradient, QColor, QPalette, QBrush
from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QProgressBar,
    QMessageBox, QScrollArea, QWidget
)
from src.app_logic.update_logic import UpdateManager


class UpdateWindow(QDialog):
    """
    Update window UI for managing application updates.
    """

    def __init__(self, update_info, update_file_url, versions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Required" if update_info is None else "Update Available")
        self.setFixedSize(400, 300)

        self.update_info = update_info or {}
        self.versions = versions
        self.update_file_url = update_file_url
        self.update_manager = None if update_file_url is None else UpdateManager(update_file_url, self.versions[1])

        self.init_ui()
        self.init_signals()

        if not self.update_file_url:
            self.update_now_btn.setEnabled(True)

    def init_ui(self):
        """Initialize the update window UI components."""
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#FFDEE9"))
        gradient.setColorAt(1, QColor("#B5FFFC"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        self.title_label = QLabel("Update Required" if not self.update_info else "Update Available",
                                  alignment=Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        version_text = f"Current Version: {self.versions[0]}\nLatest Version: {self.versions[1]}" \
            if self.update_file_url else "This version is discontinued. Please update."
        self.version_label = QLabel(version_text, alignment=Qt.AlignCenter)
        self.version_label.setStyleSheet("font-size: 14px; color: #555;")

        description_text = self.update_info.get("body", "No description available.") if self.update_info else ""
        if description_text:
            # Scrollable release description
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)

            self.description_label = QLabel(description_text)
            self.description_label.setStyleSheet("font-size: 12px; color: #444; background: #fff")
            self.description_label.setWordWrap(True)

            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.addWidget(self.description_label)
            self.scroll_area.setWidget(scroll_content)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            "QProgressBar { border-radius: 8px; height: 15px; background-color: #eee; }"
            "QProgressBar::chunk { background-color: #5cb85c; border-radius: 8px; }"
        )
        self.progress_bar.setValue(0)

        self.update_now_btn = QPushButton("Update Now")
        self.update_now_btn.setEnabled(self.update_file_url is not None)
        self.update_now_btn.setStyleSheet(
            "background-color: #5cb85c; color: white; font-size: 14px; padding: 6px; border-radius: 5px;"
        )
        self.update_now_btn.clicked.connect(self.start_update)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.version_label)
        if description_text:
            main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.update_now_btn)

        self.setLayout(main_layout)

    def init_signals(self):
        """Connect signals between the update manager and UI elements."""
        if self.update_manager:
            self.update_manager.progress_signal.connect(self.progress_bar.setValue)
            self.update_manager.download_complete_signal.connect(self.show_completion_message)

    def start_update(self):
        """Start the update process when 'Update Now' is clicked, even for discontinued versions."""
        confirm = QMessageBox.question(
            self, "Confirm Update",
            f"Are you sure you want to update to version {self.versions[1]}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        if not self.update_file_url:
            QMessageBox.information(self, "Checking for Updates", "Fetching latest update...")

            owner = "pyapril15"
            repo = "QRCodeGenerator"
            url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

            try:
                response = requests.get(url)
                response.raise_for_status()
                release_data = response.json()

                latest_update_file_url = next(
                    (asset["browser_download_url"] for asset in release_data.get("assets", []) if
                     asset["name"].endswith(".exe")),
                    None
                )

                if latest_update_file_url:
                    self.update_file_url = latest_update_file_url
                    self.update_manager = UpdateManager(self.update_file_url, release_data["tag_name"].lstrip("v"))
                    self.init_signals()
                else:
                    QMessageBox.critical(self, "Update Error", "No update file found on GitHub.")
                    return

            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "Update Error", f"Failed to fetch update: {str(e)}")
                return

        self.update_now_btn.setEnabled(False)
        self.progress_bar.setValue(0)

        if not self.update_manager:
            self.update_manager = UpdateManager(self.update_file_url, self.versions[1])
            self.init_signals()

        self.update_manager.start_update()

    def show_completion_message(self):
        """Show update completion message when download is finished."""
        QMessageBox.information(self, "Update Complete", "The update has been downloaded successfully.")
        self.close()
