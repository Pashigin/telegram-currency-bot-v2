from collectors.api_collector import fetch_rates
from collectors.scrapper_collector import collect_scrapper_data
from database.db_utils import update_api_rates, update_scrapper_rates
from datetime import datetime, UTC
from aiohttp import ClientSession


async def process_api_data():
    """
    Сервис для обработки данных из API.
    """
    async with ClientSession() as session:
        usd_rates = await fetch_rates(session, "https://open.er-api.com/v6/latest/USD")
        eur_rates = await fetch_rates(session, "https://open.er-api.com/v6/latest/EUR")

        today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

        batch_data = tuple(
            (
                currency_code,
                to_usd,
                eur_rates.get("rates", {}).get(currency_code, None),
                today,
            )
            for currency_code, to_usd in usd_rates.get("rates", {}).items()
        )

        update_api_rates(batch_data)


async def process_scrapper_data():
    """
    Сервис для обработки данных из веб-скраппера.
    """
    rates = await collect_scrapper_data()
    today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    db_data = [
        (currency_code, buy, sell, today)
        for currency_code, (buy, sell) in rates.items()
    ]

    update_scrapper_rates(db_data)
