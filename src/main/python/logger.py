import os
from datetime import datetime

from loguru import logger


def load_logger(is_test: bool = False) -> None:
    """
    Initializes the Logger.

    Args:
        is_test (bool, optional): Indicates if the logger is used for testing purposes.
    """
    # Get the current date or use a specific date for tests
    current_date = datetime.now().strftime('%Y-%m-%d')

    if is_test:
        current_date = '9999-99-99'

    # Create a file name with the date
    log_file_name = f'{current_date}_error_log.txt'
    log_file_path = os.path.join('../logs', log_file_name)

    # Configure the Loguru logger
    fmt = "{time} - {level} - {message}"
    logger.add(log_file_path, rotation="1 day", format=fmt, level="ERROR")
