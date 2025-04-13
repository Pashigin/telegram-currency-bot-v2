"""
Module for collecting currency data via web scraping.

This module scrapes exchange rates from a configured website and updates the database.

Functions:
    collect_exchange_data: Scrapes exchange rates and updates the database.
"""

import sys
import os
from datetime import UTC, datetime
from playwright.async_api import async_playwright
from database.db_utils import update_scrapper_rates
from utils.config import Config
from utils.logger import get_logger

# Ensure the module directory is in the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialize logger for this module
logger = get_logger("ScrapperCollector")


async def collect_exchange_data():
    """
    Scrapes exchange rates from a configured website and updates the database.

    Returns:
        list: A list of tuples containing currency data for database insertion.
    """
    try:
        async with async_playwright() as p:
            # Launch a headless browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to the configured URL and wait for the page to load
            await page.goto(Config.SCRAPPER_URL, wait_until="networkidle")

            # Wait for the currency data to be available on the page
            await page.wait_for_selector('ul:has(> li:has(div[class*="fc_buy"]))')
            currency_elements = await page.query_selector_all("ul > li")

            rates = {}
            for element in currency_elements:
                # Extract currency code and rates
                currency_div = await element.query_selector("div[class*='currency']")
                if not currency_div:
                    continue

                currency_text = await currency_div.text_content()
                if not currency_text or " - " not in currency_text:
                    continue

                currency_code = currency_text.split(" - ")[0].strip()[-3:]

                buy_element = await element.query_selector("div[class*='fc_buy']")
                sell_element = await element.query_selector("div[class*='fc_cell']")

                if buy_element and sell_element:
                    buy_text = await buy_element.text_content()
                    sell_text = await sell_element.text_content()

                    if buy_text and sell_text:
                        buy = float(buy_text.strip())
                        sell = float(sell_text.strip())

                        if buy > 0 and sell > 0:
                            rates[currency_code] = (1 / buy, 1 / sell)

            # Sort and log the collected rates
            sorted_rates = dict(sorted(rates.items()))
            logger.info(f"✅ Collected {len(sorted_rates)} currencies")

            # Prepare data for database insertion
            today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
            db_data = [
                (currency_code, buy, sell, today)
                for currency_code, (buy, sell) in sorted_rates.items()
            ]

            logger.debug(f"Collected rates: {rates}")
            logger.debug(f"Database data to update: {db_data}")

            # Update the database with the collected data
            await update_scrapper_rates(db_data)
            await browser.close()

        return db_data
    except Exception as e:
        # Log any errors that occur during data collection
        logger.error(f"An error occurred during data collection: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    import asyncio

    # Run the data collection function when executed as a script
    asyncio.run(collect_exchange_data())
