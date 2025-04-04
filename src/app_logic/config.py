import configparser
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Config:
    """
    Handles loading configuration settings from a config.ini file.
    Supports both source execution and packaged executable environments.
    """

    def __init__(self):
        """Initializes and loads configuration settings with error handling."""
        self._config = configparser.ConfigParser()

        # Determine base directory based on execution mode
        self._base_dir = self._get_base_directory()

        # Load configuration file
        self._config_path = os.path.join(self._base_dir, "resources", "config.ini")
        self._load_config()

        # Load resource paths
        self.qss_path = self._get_path("PATHS", "QSS_PATH")
        self.icon_path = self._get_path("PATHS", "ICON_PATH")

        # Load application settings
        self.app_name = self._get_setting("SETTINGS", "APP_NAME", fallback="QRCodeGenerator")
        self.app_version = self._get_setting("SETTINGS", "APP_VERSION", fallback="1.0.2")

        # Load QR code settings
        self.qrcode_default_version = self._get_int_setting("DEFAULT", "QRCODE_DEFAULT_VERSION", 1)
        self.qrcode_default_box_size = self._get_int_setting("DEFAULT", "QRCODE_DEFAULT_BOX_SIZE", 10)
        self.qrcode_default_border_size = self._get_int_setting("DEFAULT", "QRCODE_DEFAULT_BORDER_SIZE", 4)
        self.qrcode_default_fill_color = self._get_setting("DEFAULT", "QRCODE_DEFAULT_FILL_COLOR", fallback="#FFFFFF")
        self.qrcode_default_bg_color = self._get_setting("DEFAULT", "QRCODE_DEFAULT_BG_COLOR", fallback="#000000")

    @staticmethod
    def _get_base_directory():
        """Determines the base directory based on execution mode."""
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            return sys._MEIPASS
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def _load_config(self):
        """Loads the configuration file with error handling."""
        if not os.path.exists(self._config_path):
            logging.error(f"Configuration file not found: {self._config_path}")
            return

        try:
            self._config.read(self._config_path)
            logging.info("Configuration file loaded successfully.")
        except configparser.Error as e:
            logging.error(f"Error reading configuration file: {e}")

    def _get_setting(self, section, key, fallback=None):
        """Retrieves a setting from the configuration file with fallback."""
        try:
            return self._config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            logging.warning(f"Missing setting [{section}] {key}: {e}")
            return fallback

    def _get_int_setting(self, section, key, fallback=0):
        """Retrieves an integer setting from the configuration file with fallback."""
        try:
            return self._config.getint(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            logging.warning(f"Invalid integer setting [{section}] {key}: {e}")
            return fallback

    def _get_path(self, section, key):
        """Retrieves a file path from the configuration file and resolves its absolute path."""
        value = self._get_setting(section, key)
        return os.path.join(self._base_dir, value) if value else None


# Create a single instance of the configuration
config = Config()
