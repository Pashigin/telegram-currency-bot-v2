import sqlite3
from pathlib import Path
import aiosqlite
from contextlib import contextmanager
from utils.config import Config

DB_PATH = Config.DB_PATH


@contextmanager
def get_connection():
    Path("data").mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def update_api_rates(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            for record in data:
                currency_code, usd_to_currency, euro_to_currency, date = record

                # Check if data has changed
                cur.execute(
                    """
                    SELECT usd_to_currency, euro_to_currency, date
                    FROM api_rates
                    WHERE currency_code = ?
                    """,
                    (currency_code,),
                )
                existing = cur.fetchone()

                if not existing or existing != (
                    usd_to_currency,
                    euro_to_currency,
                    date,
                ):
                    cur.execute(
                        """
                        INSERT INTO api_rates (currency_code, usd_to_currency, euro_to_currency, date)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(currency_code)
                        DO UPDATE SET 
                            usd_to_currency = excluded.usd_to_currency,
                            euro_to_currency = excluded.euro_to_currency,
                            date = excluded.date
                        """,
                        record,
                    )
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


def update_scrapper_rates(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            for record in data:
                currency_code, buy_aed, sell_aed, date = record

                # Check if data has changed
                cur.execute(
                    """
                    SELECT buy_aed, sell_aed, date
                    FROM sharaf_exchange_rates
                    WHERE currency_code = ?
                    """,
                    (currency_code,),
                )
                existing = cur.fetchone()

                if not existing or existing != (buy_aed, sell_aed, date):
                    cur.execute(
                        """
                        INSERT INTO sharaf_exchange_rates (currency_code, buy_aed, sell_aed, date)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(currency_code)
                        DO UPDATE SET 
                            buy_aed = excluded.buy_aed,
                            sell_aed = excluded.sell_aed,
                            date = excluded.date
                        """,
                        record,
                    )
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


async def fetch_api_rates(currency_code):
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute(
                "SELECT currency_code, usd_to_currency, euro_to_currency FROM api_rates WHERE currency_code = ?",
                (currency_code,),
            ) as cursor:
                return await cursor.fetchone()
    except aiosqlite.Error as e:
        print(f"SQLite error: {e}")
        return None


async def fetch_scrapper_rates(currency_code):
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute(
                "SELECT currency_code, buy_aed, sell_aed FROM sharaf_exchange_rates WHERE currency_code = ?",
                (currency_code,),
            ) as cursor:
                return await cursor.fetchone()
    except aiosqlite.Error as e:
        print(f"SQLite error: {e}")
        return None
