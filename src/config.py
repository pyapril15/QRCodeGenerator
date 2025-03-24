import configparser
import os
import sys


class Config:
    """
    Configuration class to handle loading settings from a config.ini file.

    This class provides methods to load and access configuration settings
    from a configuration file. It handles different execution environments,
    including when the application is run from source and when it's packaged
    as an executable.
    """

    def __init__(self):
        """
        Initializes the Config class and loads configuration settings.
        """
        self.config = configparser.ConfigParser()

        #  Determine the base directory for locating resources
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            #  Running as a packaged executable
            base_dir = sys._MEIPASS
        else:
            #  Running from source
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        config_path = os.path.join(base_dir, 'resources', 'config.ini')
        self.config.read(config_path)

        #  Load paths to resources
        self.qss_path = os.path.join(base_dir, self.config.get("Paths", "QSS_PATH"))
        self.icon_path = os.path.join(base_dir, self.config.get("Paths", "ICON_PATH"))

        #  Load default settings from config.ini
        self.default_version = self.config.get('Settings', 'DEFAULT_VERSION')
        self.default_box_size = self.config.getint('Settings', 'DEFAULT_BOX_SIZE')
        self.default_border_size = self.config.getint('Settings', 'DEFAULT_BORDER_SIZE')
        self.default_fill_color = self.config.get('Settings', 'DEFAULT_FILL_COLOR')
        self.default_back_color = self.config.get('Settings', 'DEFAULT_BACK_COLOR')
        self.app_version = self.config.get('Settings', 'APP_VERSION')


config = Config()  # Initialize the configuration
