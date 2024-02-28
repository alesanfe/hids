import os
from datetime import datetime

from loguru import logger


class Logger:
    def __init__(self, is_test=False):
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

    def info(self, message):
        logger.info(message)

    def error(self, message):
        logger.error(message)

    def warning(self, message):
        logger.warning(message)
