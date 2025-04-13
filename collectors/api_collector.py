"""
Module for collecting currency data from APIs.

This module fetches currency exchange rates from configured API endpoints and updates the database.

Functions:
    fetch_rates: Fetches currency rates from a given API endpoint.
    collect_api_data: Collects currency data from APIs and prepares it for database updates.
"""

from datetime import UTC, datetime
import aiohttp
import asyncio
from utils.config import Config
from utils.logger import get_logger

# API endpoints for fetching currency rates
API_USD_URL = Config.API_USD_URL
API_EUR_URL = Config.API_EUR_URL

# Initialize logger for this module
logger = get_logger("APICollector")


async def fetch_rates(session, url):
    """
    Fetches currency rates from a given API endpoint.

    Args:
        session (aiohttp.ClientSession): The HTTP session for making requests.
        url (str): The API endpoint URL.

    Returns:
        dict: The JSON response containing currency rates, or None if the request fails.
    """
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"HTTP request failed for {url}: {e}", exc_info=True)
        return None


async def collect_api_data():
    """
    Collects currency data from APIs and prepares it for database updates.

    Returns:
        tuple: A batch of currency data ready for database insertion.
    """
    async with aiohttp.ClientSession() as session:
        # Fetch USD and EUR rates concurrently
        usd_task = fetch_rates(session, API_USD_URL)
        eur_task = fetch_rates(session, API_EUR_URL)

        usd_resp, eur_resp = await asyncio.gather(usd_task, eur_task)

        # Handle missing responses
        if usd_resp is None:
            logger.error("USD API response is None. Skipping USD rates.")
            usd_resp = {}

        if eur_resp is None:
            logger.error("EUR API response is None. Skipping EUR rates.")
            eur_resp = {}

        usd_rates = usd_resp.get("rates", {})
        eur_rates = eur_resp.get("rates", {})

        logger.info(
            f"Fetched {len(usd_rates)} USD rates and {len(eur_rates)} EUR rates from APIs."
        )

        # Prepare data for database insertion
        today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        batch_data = tuple(
            (currency_code, to_usd, eur_rates.get(currency_code, None), today)
            for currency_code, to_usd in usd_rates.items()
        )

        logger.info(
            f"Successfully prepared batch data with {len(batch_data)} entries for database update."
        )

        return batch_data
