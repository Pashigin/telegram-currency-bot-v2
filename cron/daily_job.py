import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.data_processing import process_api_data, process_scrapper_data


async def daily_job():
    await process_api_data()
    await process_scrapper_data()


if __name__ == "__main__":
    asyncio.run(daily_job())
