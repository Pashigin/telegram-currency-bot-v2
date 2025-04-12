import sqlite3
from pathlib import Path

DB_PATH = "data/currency_data.sqlite"


def get_connection():
    Path("data").mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def update_api_rates(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.executemany(
                """
                INSERT INTO api_rates (currency_code, usd_to_currency, euro_to_currency, date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(currency_code)
                DO UPDATE SET 
                    usd_to_currency = CASE 
                        WHEN api_rates.usd_to_currency != excluded.usd_to_currency THEN excluded.usd_to_currency 
                        ELSE api_rates.usd_to_currency 
                    END,
                    euro_to_currency = CASE 
                        WHEN api_rates.euro_to_currency != excluded.euro_to_currency THEN excluded.euro_to_currency 
                        ELSE api_rates.euro_to_currency 
                    END,
                    date = CASE 
                        WHEN api_rates.usd_to_currency != excluded.usd_to_currency 
                        OR api_rates.euro_to_currency != excluded.euro_to_currency 
                        THEN excluded.date 
                        ELSE api_rates.date 
                    END
                WHERE api_rates.usd_to_currency != excluded.usd_to_currency 
                OR api_rates.euro_to_currency != excluded.euro_to_currency
                """,
                data,
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


def update_scrapper_rates(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.executemany(
                """
                INSERT INTO sharaf_exchange_rates (currency_code, buy_aed, sell_aed, date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(currency_code)
                DO UPDATE SET 
                    buy_aed = CASE 
                        WHEN sharaf_exchange_rates.buy_aed != excluded.buy_aed THEN excluded.buy_aed 
                        ELSE sharaf_exchange_rates.buy_aed 
                    END,
                    sell_aed = CASE 
                        WHEN sharaf_exchange_rates.sell_aed != excluded.sell_aed THEN excluded.sell_aed 
                        ELSE sharaf_exchange_rates.sell_aed 
                    END,
                    date = CASE 
                        WHEN sharaf_exchange_rates.buy_aed != excluded.buy_aed 
                        OR sharaf_exchange_rates.sell_aed != excluded.sell_aed 
                        THEN excluded.date 
                        ELSE sharaf_exchange_rates.date 
                    END
                WHERE sharaf_exchange_rates.buy_aed != excluded.buy_aed 
                OR sharaf_exchange_rates.sell_aed != excluded.sell_aed
                """,
                data,
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")


def fetch_api_rates(currency_code):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT currency_code, usd_to_currency, euro_to_currency FROM api_rates WHERE currency_code = ?",
                (currency_code,),
            )
            return cur.fetchone()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None


def fetch_scrapper_rates(currency_code):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT currency_code, buy_aed, sell_aed FROM sharaf_exchange_rates WHERE currency_code = ?",
                (currency_code,),
            )
            return cur.fetchone()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
