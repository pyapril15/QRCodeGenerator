import logging
import os


def setup_logger() -> logging.Logger:
    """
    Sets up a logger with console and file handlers.

    This function configures a logger that outputs logs to both the console
    and a file. It returns a configured logger object.

    Returns:
        logging.Logger: A configured logger object.
    """
    log = logging.getLogger(__name__)  # Use __name__ for module-specific logs
    log.setLevel(logging.DEBUG)

    #  Ensure log directory exists
    log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(log_dir, exist_ok=True)  # Create directory if it doesn't exist
    log_path = os.path.join(log_dir, 'app.log')

    #  Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_path)

    c_handler.setLevel(logging.WARNING)  # Console handler level
    f_handler.setLevel(logging.DEBUG)  # File handler level

    #  Create formatters and add them to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    #  Add handlers to the logger
    log.addHandler(c_handler)
    log.addHandler(f_handler)

    return log


logger = setup_logger()  # Initialize the logger
