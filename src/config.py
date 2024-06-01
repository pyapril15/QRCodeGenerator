import configparser
import os


class Config:
    """
    Configuration class to handle loading settings from config.ini file.
    """

    def __init__(self):
        """
        Initialize Config class.
        """
        self.config = configparser.ConfigParser()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(self.base_dir, 'resources', 'config.ini')
        self.config.read(config_path)

        # Load paths from config.ini
        self.qss_path = os.path.join(self.base_dir, self.config.get("Paths", "QSS_PATH"))
        self.icon_path = os.path.join(self.base_dir, self.config.get("Paths", "ICON_PATH"))

        # Load default settings from config.ini
        self.default_version = self.config.getint('Settings', 'DEFAULT_VERSION')
        self.default_box_size = self.config.getint('Settings', 'DEFAULT_BOX_SIZE')
        self.default_border_size = self.config.getint('Settings', 'DEFAULT_BORDER_SIZE')
        self.default_fill_color = self.config.get('Settings', 'DEFAULT_FILL_COLOR')
        self.default_back_color = self.config.get('Settings', 'DEFAULT_BACK_COLOR')


config = Config()
