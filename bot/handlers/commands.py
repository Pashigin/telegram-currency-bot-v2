"""
Command handlers for the Telegram bot.

This module defines the commands and their respective handlers for interacting with the bot.

Functions:
    handle_send_welcome: Handles the '/start' and '/help' commands.
    handle_get_api_rates: Handles the command to check official currency rates.
    handle_get_scrapper_rates: Handles the command to check exchange rates from scrappers.
    handle_update_rates: Handles the command to update currency rates.
    handle_send_help: Handles the 'help' command.
    handle_check_rates_command: Handles the '/check_rates' command.
    handle_check_exchange_command: Handles the '/check_exchange' command.
    handle_update_rates_command: Handles the '/update_rates' command.
    handle_check_command: Handles the '/check' command for currency conversion.
"""

from ..config import bot, create_markup
from .. import logger
from .async_functions import (
    send_welcome,
    get_api_rates,
    get_scrapper_rates,
    update_rates,
    send_help,
    check_currency,
)

# Create a keyboard markup for the bot's interface
markup = create_markup()


@bot.message_handler(commands=["start", "help"])
async def handle_send_welcome(message):
    """
    Handles the '/start' and '/help' commands by sending a welcome message.

    Args:
        message: The message object from the user.
    """
    try:
        logger.info("Handling 'start' or 'help' command.")
        await send_welcome(message)
    except Exception as e:
        logger.error(f"Error in handle_send_welcome: {e}", exc_info=True)


@bot.message_handler(func=lambda message: message.text == "Проверить оф. курсы валют")
async def handle_get_api_rates(message):
    """
    Handles the command to check official currency rates.

    Args:
        message: The message object from the user.
    """
    logger.info("Handling 'check official rates' command.")
    await get_api_rates(message)


@bot.message_handler(func=lambda message: message.text == "Проверить курс обменника")
async def handle_get_scrapper_rates(message):
    """
    Handles the command to check exchange rates from scrappers.

    Args:
        message: The message object from the user.
    """
    logger.info("Handling 'check exchange rates' command.")
    await get_scrapper_rates(message)


@bot.message_handler(func=lambda message: message.text == "Обновить курсы валют")
async def handle_update_rates(message):
    """
    Handles the command to update currency rates.

    Args:
        message: The message object from the user.
    """
    logger.info("Handling 'update rates' command.")
    await update_rates(message)


@bot.message_handler(func=lambda message: message.text == "Помощь")
async def handle_send_help(message):
    """
    Handles the 'help' command by sending a help message.

    Args:
        message: The message object from the user.
    """
    logger.info("Handling 'help' command.")
    await send_help(message)


@bot.message_handler(commands=["check_rates"])
async def handle_check_rates_command(message):
    """
    Handles the '/check_rates' command by fetching and sending official rates.

    Args:
        message: The message object from the user.
    """
    await get_api_rates(message)


@bot.message_handler(commands=["check_exchange"])
async def handle_check_exchange_command(message):
    """
    Handles the '/check_exchange' command by fetching and sending exchange rates.

    Args:
        message: The message object from the user.
    """
    await get_scrapper_rates(message)


@bot.message_handler(commands=["update_rates"])
async def handle_update_rates_command(message):
    """
    Handles the '/update_rates' command by updating currency rates.

    Args:
        message: The message object from the user.
    """
    await update_rates(message)


@bot.message_handler(commands=["check"])
async def handle_check_command(message):
    """
    Handles the '/check' command for currency conversion.

    Args:
        message: The message object from the user.
    """
    await check_currency(message)
