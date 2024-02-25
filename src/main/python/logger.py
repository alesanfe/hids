import os
from datetime import datetime

from loguru import logger


class Logger:
    def __init__(self):
        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Create a file name with the date
        log_file_name = f'{current_date}_log.txt'
        log_file_path = os.path.join('../logs', log_file_name)

        # Configure the Loguru logger
        fmt = "{time} - {level} - {message}"
        logger.add(log_file_path, rotation="1 day", format=fmt)

    def info(self, message):
        logger.info(message)

    def error(self, message):
        logger.error(message)

    def warning(self, message):
        logger.warning(message)
