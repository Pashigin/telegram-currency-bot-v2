"""
Database utilities module.

This module provides asynchronous functions for interacting with the database,
including updating and fetching currency rates from API and scrapper sources.

Functions:
    update_api_rates: Updates API rates in the database.
    update_scrapper_rates: Updates scrapper rates in the database.
    fetch_api_rates: Fetches API rates for a given currency code.
    fetch_scrapper_rates: Fetches scrapper rates for a given currency code.
"""

from database.db_helpers import fetch_rates, update_rates
from utils.config import Config
from utils.logger import (
    get_logger,
)  # Import directly from utils.logger instead of database

# Create logger for this module
logger = get_logger(__name__)

# Path to the SQLite database file
DB_PATH = Config.DB_PATH


async def update_api_rates(data):
    """
    Updates API rates in the database asynchronously.

    Args:
        data (list of tuples): Each tuple contains currency code, USD rate, Euro rate, and date.
    """
    try:
        logger.debug(f"Data received for update: {data}")
        filtered_data = data

        if filtered_data:
            # Update the database with the provided API rates
            await update_rates(
                "api_rates",
                ["currency_code", "usd_to_currency", "euro_to_currency", "date"],
                filtered_data,
            )
            # No need to log here as it's already logged in update_rates
        else:
            logger.info("No API rates were updated.")
        return []
    except Exception as e:
        # Log any errors that occur during the update operation
        logger.error(f"Error in update_api_rates: {e}", exc_info=True)


async def update_scrapper_rates(data):
    """
    Updates scrapper rates in the database asynchronously.

    Args:
        data (list of tuples): Each tuple contains currency code, buy AED rate, sell AED rate, and date.
    """

    if data:
        # Log only at debug level to avoid duplication with db_helpers
        logger.debug(f"Updating scrapper rates: {len(data)} currencies to update.")
        # Update the database with the provided scrapper rates
        await update_rates(
            "sharaf_exchange_rates",
            ["currency_code", "buy_aed", "sell_aed", "date"],
            data,
        )
        # No need to log here as it's already logged in update_rates
    else:
        logger.info("No scrapper rates were updated.")


async def fetch_api_rates(currency_code):
    """
    Fetches API rates for a given currency code.

    Args:
        currency_code (str): The currency code to fetch rates for.

    Returns:
        tuple: A tuple containing currency code, USD rate, and Euro rate, or None if no data is found.
    """
    return await fetch_rates(
        "api_rates",
        ["currency_code", "usd_to_currency", "euro_to_currency"],
        "currency_code",
        currency_code,
    )


async def fetch_scrapper_rates(currency_code):
    """
    Fetches scrapper rates for a given currency code.

    Args:
        currency_code (str): The currency code to fetch rates for.

    Returns:
        tuple: A tuple containing currency code, buy AED rate, and sell AED rate, or None if no data is found.
    """
    return await fetch_rates(
        "sharaf_exchange_rates",
        ["currency_code", "buy_aed", "sell_aed"],
        "currency_code",
        currency_code,
    )
