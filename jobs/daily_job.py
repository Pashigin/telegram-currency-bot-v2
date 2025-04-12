from collectors.api_collector import collect_api_data
from collectors.scrapper_collector import collect_exchange_data

import asyncio


async def daily_job():
    await collect_api_data()
    await collect_exchange_data()


if __name__ == "__main__":
    asyncio.run(daily_job())
