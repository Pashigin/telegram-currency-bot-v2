"""
Asynchronous functions for the Telegram bot.

This module contains the logic for each asynchronous command used in the bot.

Functions:
    send_welcome: Sends a welcome message to the user.
    get_api_rates: Fetches and sends official currency rates.
    get_scrapper_rates: Fetches and sends exchange rates from scrappers.
    update_rates: Updates currency rates and notifies the user.
    send_help: Sends a help message with available commands.
    check_currency: Checks and sends currency conversion rates.
"""

from ..config import bot
from .. import logger
from database.db_utils import fetch_api_rates, fetch_scrapper_rates
from jobs.daily_job import daily_job
from utils.formatters import (
    format_api_currency_response,
    format_scrapper_currency_response,
    format_help_message,
    format_check_currency_response,
)

# Placeholder for keyboard markup, if needed
markup = None

# Error messages for various scenarios
ERROR_FETCHING_RATES = (
    "❌ Не удалось получить официальные курсы валют. Пожалуйста, попробуйте позже."
)
ERROR_FETCHING_SCRAPPER_RATES = (
    "❌ Не удалось получить курсы обмена. Пожалуйста, попробуйте позже."
)
ERROR_UPDATE_DAILY_RATES = (
    "❌ Не удалось обновить курсы валют. Пожалуйста, попробуйте позже."
)
ERROR_INVALID_CURRENCY = "❌ Неверный код валюты. Валюта отсутствует в базе данных."


async def send_welcome(message):
    """
    Sends a welcome message to the user and provides help information.

    Args:
        message: The message object from the user.
    """
    logger.info(f"Executing function: {message.text}")
    user_name = message.from_user.first_name
    await bot.send_message(
        message.chat.id,
        f"Привет, {user_name}!",
        reply_markup=markup,
    )
    await bot.send_message(chat_id=message.chat.id, text=format_help_message())


async def get_api_rates(message):
    """
    Fetches and sends official currency rates to the user.

    Args:
        message: The message object from the user.
    """
    logger.info(f"Executing function: {message.text}")
    try:
        rates = await fetch_api_rates("AED")
        response = (
            format_api_currency_response(rates) if rates else ERROR_FETCHING_RATES
        )
        if not rates:
            logger.warning("Failed to fetch API rates")
        await bot.send_message(chat_id=message.chat.id, text=response)
    except Exception as e:
        logger.error(f"Error in get_api_rates: {e}", exc_info=True)
        await bot.send_message(chat_id=message.chat.id, text=ERROR_FETCHING_RATES)


async def get_scrapper_rates(message):
    """
    Fetches and sends exchange rates from scrappers to the user.

    Args:
        message: The message object from the user.
    """
    logger.info(f"Executing function: {message.text}")
    usd_rate = await fetch_scrapper_rates("USD")
    eur_rate = await fetch_scrapper_rates("EUR")

    if not usd_rate or not eur_rate:
        logger.warning("Failed to fetch scrapper rates")

    usd_rate_tuple = (usd_rate[0], usd_rate[1], usd_rate[2]) if usd_rate else None
    eur_rate_tuple = (eur_rate[0], eur_rate[1], eur_rate[2]) if eur_rate else None

    response = (
        format_scrapper_currency_response(usd_rate_tuple, eur_rate_tuple)
        if usd_rate and eur_rate
        else ERROR_FETCHING_SCRAPPER_RATES
    )
    await bot.send_message(chat_id=message.chat.id, text=response)


async def update_rates(message):
    """
    Updates currency rates and notifies the user.

    Args:
        message: The message object from the user.
    """
    logger.info(f"Executing function: {message.text}")
    await bot.send_message(
        message.chat.id,
        "⏳ Обновляю данные, подождите минуточку...",
        reply_markup=markup,
    )
    await daily_job()
    response = "✅ Данные успешно обновлены!"
    logger.info("Daily rates updated successfully")

    await bot.send_message(chat_id=message.chat.id, text=response)
    return response


async def send_help(message):
    """
    Sends a help message with available commands to the user.

    Args:
        message: The message object from the user.
    """
    logger.info(f"Executing function: {message.text}")
    await bot.send_message(chat_id=message.chat.id, text=format_help_message())


async def check_currency(message):
    """
    Checks and sends currency conversion rates to the user.

    Args:
        message: The message object from the user.
    """
    logger.info(f"Executing function: {message.text}")

    # Extract currency code or prompt user if not provided
    try:
        currency_code = message.text.split()[1].upper()
    except IndexError:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Пожалуйста, укажите код валюты после команды. Пример: /check USD",
        )
        return

    # Fetch rates from API and scrapper
    api_rate = await fetch_api_rates(currency_code)
    scrapper_rate = await fetch_scrapper_rates(currency_code)

    # Handle cases where currency is not found in either source
    if not api_rate and not scrapper_rate:
        logger.warning("Currency not found in any database: %s", currency_code)
        await bot.send_message(chat_id=message.chat.id, text=ERROR_INVALID_CURRENCY)
        return

    # Format response based on available data
    if api_rate:
        usd_to_currency, eur_to_currency = api_rate[1:3]
    else:
        usd_to_currency = eur_to_currency = None

    if scrapper_rate:
        scrapper_buy, scrapper_sell = scrapper_rate[1:3]
    else:
        scrapper_buy = scrapper_sell = None

    response = format_check_currency_response(
        currency_code,
        (usd_to_currency, eur_to_currency) if api_rate else None,
        (scrapper_buy, scrapper_sell) if scrapper_rate else None,
    )

    await bot.send_message(chat_id=message.chat.id, text=response)
