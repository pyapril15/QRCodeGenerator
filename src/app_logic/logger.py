import logging
import os


class Logger:
    """
    Logger setup class to configure logging for the application.
    Supports both console and file logging with different log levels.
    """

    LOG_FILE_NAME = "app.log"

    def __init__(self):
        """Initializes the logger with console and file handlers."""
        self._logger = logging.getLogger("QRCodeGenerator")
        self._logger.setLevel(logging.DEBUG)

        # Prevent duplicate handlers in case of multiple logger instances
        if not self._logger.hasHandlers():
            self._setup_handlers()

    def _setup_handlers(self):
        """Sets up logging handlers for console and file logging."""
        log_dir = self._get_log_directory()
        log_file_path = os.path.join(log_dir, self.LOG_FILE_NAME)

        try:
            os.makedirs(log_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating log directory: {e}")

        # Console handler (Warning and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_format)

        # File handler (Logs everything)
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_format)

        # Attach handlers to logger
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

    @staticmethod
    def _get_log_directory():
        """Determines and returns the correct log directory path."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        return base_dir

    def get_logger(self):
        """Returns the configured logger instance."""
        return self._logger


# Create and expose a single logger instance
logger = Logger().get_logger()
