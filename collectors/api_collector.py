import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import aiohttp
import asyncio
from datetime import UTC, datetime
from database.db_utils import update_api_rates


API_USD_URL = "https://open.er-api.com/v6/latest/USD"
API_EUR_URL = "https://open.er-api.com/v6/latest/EUR"


async def fetch_rates(session, url):
    async with session.get(url) as response:
        return await response.json()


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
        print("❌ Ошибка при сборе API данных:", e)


# Удаляю вызов collect_api_data в блоке __main__
if __name__ == "__main__":
    print("This module is now used as a utility for fetching API data.")
