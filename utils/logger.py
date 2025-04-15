"""
Logger configuration module for Telegram Currency Bot.

This module provides a function for getting a preconfigured logger instance
that outputs information both to the console and to a file.

Functions:
    get_logger: Returns a configured logger instance.
"""

import logging


def get_logger(name, log_file="bot.log", level=logging.INFO):
    """
    Returns a configured logger instance with output to console and file.

    Args:
        name (str): The name of the logger.
        log_file (str): The file to which logs will be written.
        level (int): The logging level.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent logs from being passed to the root logger to avoid duplication
    logger.propagate = False

    # Add handlers only if they don't already exist
    if not logger.handlers:
        # Handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(console_handler)

        # Handler for file output
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

    return logger
