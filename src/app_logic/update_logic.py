import threading

import requests
from PySide6.QtCore import QObject, Signal


class UpdateManager(QObject):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    download_complete_signal = Signal()
    restart_signal = Signal()

    def __init__(self, update_file_url, version):
        super().__init__()
        self.update_file_url = update_file_url
        self.update_file_name = f"QRCodeGenerator_{version}.exe"

    def start_update(self):
        """Starts update download in a separate thread."""
        threading.Thread(target=self.download_update, daemon=True).start()

    def download_update(self):
        """Handles downloading and progress updates."""
        try:
            session = requests.Session()
            response = session.get(self.update_file_url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(self.update_file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.progress_signal.emit(int((downloaded / total_size) * 100))

            self.download_complete_signal.emit()

        except Exception as e:
            self.status_signal.emit(f"Update failed: {str(e)}")

    def close_application(self):
        """Triggers restart message before closing."""
        self.restart_signal.emit()
