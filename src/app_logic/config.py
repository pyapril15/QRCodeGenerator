import configparser
import os
import sys


class Config:
    """
    Handles loading configuration settings from a config.ini file.

    Supports both source execution and packaged executable environments.
    """

    def __init__(self):
        """Initializes and loads configuration settings."""
        self.config = configparser.ConfigParser()

        # Determine base directory based on execution mode
        base_dir = (
            sys._MEIPASS if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
            else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )


        # Load configuration file
        config_path = os.path.join(base_dir, "resources", "config.ini")
        self.config.read(config_path)

        # Load resource paths
        self.qss_path = os.path.join(base_dir, self.config.get("Paths", "QSS_PATH"))
        self.icon_path = os.path.join(base_dir, self.config.get("Paths", "ICON_PATH"))

        # Load application settings
        self.default_version = self.config.getint("Settings", "DEFAULT_VERSION")
        self.default_box_size = self.config.getint("Settings", "DEFAULT_BOX_SIZE")
        self.default_border_size = self.config.getint("Settings", "DEFAULT_BORDER_SIZE")
        self.default_fill_color = self.config.get("Settings", "DEFAULT_FILL_COLOR")
        self.default_back_color = self.config.get("Settings", "DEFAULT_BACK_COLOR")
        self.app_version = self.config.get("Settings", "APP_VERSION")


config = Config()  # Initialize configuration instance
