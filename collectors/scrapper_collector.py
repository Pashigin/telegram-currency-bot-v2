"""
Module for collecting currency data via web scraping.

This module scrapes exchange rates from a configured website and returns the data.

Functions:
    collect_exchange_data: Scrapes exchange rates and returns the data.
"""

from datetime import UTC, datetime
from playwright.async_api import async_playwright
from utils.config import Config
from utils.logger import (
    get_logger,
)  # Import directly from utils.logger instead of collectors

# Create logger for this module
logger = get_logger(__name__)


async def collect_exchange_data():
    """
    Scrapes exchange rates from a configured website.

    Returns:
        list: A list of tuples containing currency data for database insertion.
        Returns None if an error occurs.
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
            logger.info(f"Collected {len(sorted_rates)} currencies")

            # Prepare data for database insertion
            today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
            db_data = [
                (currency_code, buy, sell, today)
                for currency_code, (buy, sell) in sorted_rates.items()
            ]

            logger.debug(f"Collected rates: {rates}")
            logger.debug(f"Database data prepared: {db_data}")

            await browser.close()
            return db_data
    except Exception as e:
        # Log any errors that occur during data collection
        logger.error(f"An error occurred during data collection: {e}", exc_info=True)
        return None
