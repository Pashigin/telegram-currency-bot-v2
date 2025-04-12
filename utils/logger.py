"""
Logger configuration for the Telegram Currency Bot.

This module provides a utility function to get a pre-configured logger instance.
"""

import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name):
    """
    Returns a configured logger instance.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(name)
