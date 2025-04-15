"""
Configuration module for environment variables.

This module loads environment variables using the `dotenv` package and provides
access to configuration values such as API URLs, database paths, and Telegram tokens.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for storing application settings.

    All configuration values are loaded from environment variables,
    with defaults provided for some values.
    """

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_TOKEN_TEST = os.getenv("TELEGRAM_TOKEN_TEST")
    DB_PATH = os.getenv("DB_PATH", "data/currency_data.sqlite")
    API_USD_URL = os.getenv("API_USD_URL", "https://open.er-api.com/v6/latest/USD")
    API_EUR_URL = os.getenv("API_EUR_URL", "https://open.er-api.com/v6/latest/EUR")
    SCRAPPER_URL = os.getenv(
        "SCRAPPER_URL", "https://www.sharafexchange.ae/services/currency-exchange"
    )
