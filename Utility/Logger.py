import config
import logging
from datetime import datetime


class Logger:
    @staticmethod
    def get_logger(filename: str) -> logging.Logger:
        timestamp = datetime.now().strftime("[%m-%d-%Y %H-%M-%S]")
        log_path = config.LOG_DIR.joinpath(f"{timestamp} {filename}")

        logger = logging.getLogger()
        logger.addHandler(logging.FileHandler(log_path))
        logger.setLevel(logging.INFO)
        return logger
