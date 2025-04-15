"""
Configuration and initialization for the Telegram bot.

This module sets up the bot instance and provides utility functions like creating a keyboard markup.

Attributes:
    bot (AsyncTeleBot): The bot instance initialized with the Telegram token.

Functions:
    create_markup: Creates a keyboard markup for the bot's interface.
"""

from telebot.async_telebot import AsyncTeleBot
from telebot import types
from utils.config import Config
from utils.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

try:
    # Retrieve the Telegram token from the configuration
    TELEGRAM_TOKEN = Config.TELEGRAM_TOKEN_TEST
    if TELEGRAM_TOKEN is None:
        raise ValueError("TELEGRAM_TOKEN cannot be None")

    # Initialize the bot instance
    bot = AsyncTeleBot(TELEGRAM_TOKEN)
except Exception as e:
    # Log and raise any errors during bot initialization
    logger.error(f"Failed to initialize bot: {e}", exc_info=True)
    raise


def create_markup():
    """
    Creates a keyboard markup for the bot's interface.

    Returns:
        types.ReplyKeyboardMarkup: A keyboard markup with predefined buttons.
    """
    # Create a keyboard markup with buttons for various bot commands
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Check official currency rates"),
        types.KeyboardButton("Check exchange rates"),
    )
    markup.add(
        types.KeyboardButton("Update currency rates"), types.KeyboardButton("Help")
    )
    return markup
