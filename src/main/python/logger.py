from datetime import datetime
from loguru import logger
import os

class Logger:
    """
    Class for managing logging functionality.
    """

    def __init__(self, is_test: bool = False) -> None:
        """
        Initializes the Logger class.

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

    def info(self, message: str) -> None:
        """
        Logs an information message.

        Args:
            message (str): The information message to be logged.
        """
        logger.info(message)

    def error(self, message: str) -> None:
        """
        Logs an error message.

        Args:
            message (str): The error message to be logged.
        """
        logger.error(message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message (str): The warning message to be logged.
        """
        logger.warning(message)
