from playwright.async_api import async_playwright
from datetime import datetime, UTC
from database.db_utils import update_scrapper_rates
from utils.config import Config
from .base_collector import BaseCollector


class ScrapperCollector(BaseCollector):
    """Сборщик данных через веб-скрапинг."""

    async def collect_data(self) -> None:
        """Реализация метода для сбора данных через веб-скрапинг."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(
                    Config.SCRAPPER_URL,  # Use SCRAPPER_URL from config
                    wait_until="networkidle",
                )

                # Ждем загрузку таблицы, используя проверенный селектор
                await page.wait_for_selector('ul:has(> li:has(div[class*="fc_buy"]))')
                currency_elements = await page.query_selector_all("ul > li")

                rates = {}
                for element in currency_elements:
                    try:
                        # Получаем код валюты из div с классом currency
                        currency_div = await element.query_selector(
                            "div[class*='currency']"
                        )
                        if not currency_div:
                            continue

                        currency_text = await currency_div.text_content()
                        currency_code = currency_text.split(" - ")[0].strip()[-3:]  # type: ignore

                        # Получаем курсы напрямую по классам
                        buy_element = await element.query_selector(
                            "div[class*='fc_buy']"
                        )
                        sell_element = await element.query_selector(
                            "div[class*='fc_cell']"
                        )

                        if buy_element and sell_element:
                            buy = float((await buy_element.text_content()).strip())  # type: ignore
                            sell = float((await sell_element.text_content()).strip())  # type: ignore

                            if buy > 0 and sell > 0:
                                rates[currency_code] = (1 / buy, 1 / sell)

                    except (ValueError, TypeError, AttributeError) as e:
                        print(f"Error processing currency: {e}")
                        continue

                # Sort rates by currency code
                sorted_rates = dict(sorted(rates.items()))
                print(f"✅ Collected {len(sorted_rates)} currencies")

                # Convert sorted rates to database format and update
                today = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
                db_data = [
                    (currency_code, buy, sell, today)
                    for currency_code, (buy, sell) in sorted_rates.items()
                ]

                update_scrapper_rates(db_data)

            except Exception as e:
                print(f"❌ Error: {e}")
            finally:
                await browser.close()


if __name__ == "__main__":
    print("This module is now used as a utility for scraping data.")
