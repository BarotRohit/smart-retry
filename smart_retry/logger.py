import logging
import os

def get_logger(log_file=None):
    """Creates a logger that writes to file or console."""
    # Create unique logger name based on log_file to avoid conflicts
    logger_name = f"smart_retry_{log_file}" if log_file else "smart_retry_console"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if already exists
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if log_file:
        # Ensure the directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
