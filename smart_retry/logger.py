import logging

def get_logger(log_file=None):
    """Creates a logger that writes to file or console."""
    logger = logging.getLogger("smart_retry")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if already exists
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
