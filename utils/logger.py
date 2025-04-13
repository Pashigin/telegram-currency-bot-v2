"""
Logger configuration for the Telegram Currency Bot.

This module provides a utility function to get a pre-configured logger instance.
"""

import logging


def get_logger(name, log_file="bot.log", level=logging.INFO):
    """
    Returns a configured logger instance that logs to both console and file.

    Args:
        name (str): The name of the logger.
        log_file (str): The file to which logs will be written.
        level (int): The logging level.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

    return logger
