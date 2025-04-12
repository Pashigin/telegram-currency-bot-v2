import logging
from datetime import UTC, datetime

import aiohttp
import asyncio

from database.db_utils import update_api_rates
from utils.config import Config

API_USD_URL = Config.API_USD_URL
API_EUR_URL = Config.API_EUR_URL

# Replace print statements with logging
logger = logging.getLogger("APICollector")


async def fetch_rates(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"HTTP error while fetching rates from {url}: {e}")
        return {}
    except asyncio.TimeoutError:
        logger.error(f"Timeout error while fetching rates from {url}")
        return {}


async def collect_api_data():
    try:
        async with aiohttp.ClientSession() as session:
            usd_task = fetch_rates(session, API_USD_URL)
            eur_task = fetch_rates(session, API_EUR_URL)

            # Параллельное выполнение запросов
            usd_resp, eur_resp = await asyncio.gather(usd_task, eur_task)

            usd_rates = usd_resp.get("rates", {})
            eur_rates = eur_resp.get("rates", {})

            today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

            batch_data = tuple(
                (currency_code, to_usd, eur_rates.get(currency_code, None), today)
                for currency_code, to_usd in usd_rates.items()
            )

            update_api_rates(batch_data)
    except Exception as e:
        logger.error("❌ Ошибка при сборе API данных:", exc_info=e)


if __name__ == "__main__":
    print("This module is now used as a utility for fetching API data.")
