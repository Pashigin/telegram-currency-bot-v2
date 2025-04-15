"""
Database package for the currency bot.

This package contains database models and utilities for storing and retrieving currency data.
"""

from utils.logger import get_logger
from .db_helpers import update_rates, fetch_rates
from .db_utils import (
    update_api_rates,
    update_scrapper_rates,
    fetch_api_rates,
    fetch_scrapper_rates,
)

logger = get_logger(__name__)

__all__ = [
    "update_rates",
    "fetch_rates",
    "update_api_rates",
    "update_scrapper_rates",
    "fetch_api_rates",
    "fetch_scrapper_rates",
]
