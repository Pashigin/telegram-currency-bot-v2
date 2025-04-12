from collectors.api_collector import fetch_rates
from collectors.scrapper_collector import ScrapperCollector
from database.db_utils import update_api_rates
from datetime import datetime, UTC
from aiohttp import ClientSession


async def fetch_and_process_api_data(session, url, eur_rates, today):
    usd_rates = await fetch_rates(session, url)
    return tuple(
        (
            currency_code,
            to_usd,
            eur_rates.get("rates", {}).get(currency_code, None),
            today,
        )
        for currency_code, to_usd in usd_rates.get("rates", {}).items()
    )


async def process_api_data():
    """
    Сервис для обработки данных из API.
    """
    async with ClientSession() as session:
        eur_rates = await fetch_rates(session, "https://open.er-api.com/v6/latest/EUR")
        today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

        batch_data = await fetch_and_process_api_data(
            session, "https://open.er-api.com/v6/latest/USD", eur_rates, today
        )

        update_api_rates(batch_data)


async def process_scrapper_data():
    """
    Сервис для обработки данных из веб-скраппера.
    """
    scrapper = ScrapperCollector()
    await scrapper.collect_data()
    today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    # Assuming rates are stored in the database by collect_data
    print(f"Data processed and stored on {today}")
