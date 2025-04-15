"""
Telegram bot handlers module.

This package contains command handlers and async functions for the Telegram bot.
"""

from utils.logger import get_logger
from .commands import *
from .async_functions import (
    send_welcome,
    get_api_rates,
    get_scrapper_rates,
    update_rates,
    send_help,
    check_currency,
)

logger = get_logger(__name__)
