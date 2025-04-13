"""
Executes daily tasks for collecting currency data.

This script collects data from both API and web scrapers and updates the database.

Functions:
    daily_job: Collects currency data from APIs and scrapers, then updates the database.
"""

import sys
import os
from collectors.api_collector import collect_api_data
from collectors.scrapper_collector import collect_exchange_data
from utils.logger import get_logger
from database.db_utils import update_api_rates, update_scrapper_rates
import asyncio

# Ensure the module directory is in the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialize logger for this module
logger = get_logger("DailyJob")


async def daily_job():
    """
    Collects currency data from APIs and web scrapers, then updates the database.

    This function performs the following steps:
        1. Collects data from APIs and updates the database.
        2. Collects data from web scrapers and updates the database.
        3. Logs warnings if data collection fails.
    """
    try:
        logger.info("Starting daily job execution")

        # Collect and update API data
        api_data = await collect_api_data()
        if api_data:
            await update_api_rates(api_data)

        # Collect and update scrapper data
        scrapper_data = await collect_exchange_data()
        if scrapper_data:
            await update_scrapper_rates(scrapper_data)

        # Log a warning if no data was collected
        if not api_data or not scrapper_data:
            logger.warning("Skipped updates due to empty data collection.")

        logger.info("Daily job execution completed")
    except Exception as e:
        # Log any errors that occur during the daily job
        logger.error(f"Error in daily_job: {e}", exc_info=True)


if __name__ == "__main__":
    # Run the daily job when executed as a script
    asyncio.run(daily_job())
