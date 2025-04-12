"""
Database models and table creation for the Telegram Currency Bot.

This module defines the database schema and provides a function to create necessary tables.
"""

import sqlite3
from utils.config import Config

DB_PATH = Config.DB_PATH


def create_tables():
    """
    Creates the necessary database tables if they do not already exist.

    Tables:
        - api_rates: Stores official currency rates.
        - sharaf_exchange_rates: Stores exchange rates from Sharaf Exchange.

    Raises:
        sqlite3.Error: If an error occurs during table creation.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Таблица для API
        cur.execute("""
        CREATE TABLE IF NOT EXISTS api_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT NOT NULL UNIQUE,
            usd_to_currency REAL,
            euro_to_currency REAL,
            date TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_api_currency_code ON api_rates(currency_code);
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sharaf_exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT NOT NULL UNIQUE,
            buy_aed REAL,
            sell_aed REAL,
            date TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sharaf_currency_code ON sharaf_exchange_rates(currency_code);
        """)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
