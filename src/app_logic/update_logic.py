import threading
import requests
from PySide6.QtCore import QObject, Signal


class UpdateManager(QObject):
    """Handles update checking, downloading, and installation processes."""

    progress_signal = Signal(int)
    status_signal = Signal(str)
    download_complete_signal = Signal()
    restart_signal = Signal()

    def __init__(self, update_file_url, version):
        super().__init__()
        self.update_file_url = update_file_url
        self.update_file_name = f"QRCodeGenerator_{version}.exe"

    def start_update(self):
        """Starts the update download in a separate thread."""
        threading.Thread(target=self.download_update, daemon=True).start()

    def download_update(self):
        """Handles downloading the update and updating progress signals."""
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


def check_for_updates(config, logger, update_callback):
    """Checks for application updates and fetches latest version if discontinued."""
    try:
        current_version = config.app_version
        owner = "pyapril15"
        repo = "QRCodeGenerator"

        url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        response = requests.get(url)
        response.raise_for_status()
        releases = response.json()

        # Get the latest release details
        latest_release = releases[0] if releases else None
        latest_version = latest_release["tag_name"].lstrip("v") if latest_release else None

        # Find the latest available .exe update file
        latest_update_file_url = None
        for release in releases:
            for asset in release.get("assets", []):
                if asset["name"].endswith(".exe"):
                    latest_update_file_url = asset["browser_download_url"]
                    break
            if latest_update_file_url:
                break

        if not latest_update_file_url:
            logger.error("No .exe update file found in any releases.")
            return

        if latest_version and latest_version > current_version:
            logger.info(f"New update available: {latest_version}")
            update_callback(latest_release, latest_update_file_url, (current_version, latest_version))
        else:
            logger.info("No update required.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking for updates: {str(e)}")


def is_version_discontinued(config):
    """Checks if the current version is discontinued on GitHub."""
    try:
        owner = "pyapril15"
        repo = "QRCodeGenerator"

        url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        response = requests.get(url)
        response.raise_for_status()
        releases = response.json()

        available_versions = {release["tag_name"].lstrip("v") for release in releases}
        return config.app_version not in available_versions
    except requests.exceptions.RequestException:
        return False
