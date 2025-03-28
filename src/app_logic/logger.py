import logging
import os


def setup_logger() -> logging.Logger:
    """
    Configures a logger with both console and file handlers.

    The console handler logs warnings and above, while the file handler logs all messages.
    Ensures the log directory exists before writing to the log file.

    Returns:
        logging.Logger: A configured logger instance.
    """
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    # Determine log file path
    log_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    # Create console and file handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_path)

    c_handler.setLevel(logging.WARNING)  # Console logs warnings and errors
    f_handler.setLevel(logging.DEBUG)  # File logs all levels

    # Define log formats
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Attach handlers to logger
    log.addHandler(c_handler)
    log.addHandler(f_handler)

    return log


logger = setup_logger()  # Initialize logger instance
