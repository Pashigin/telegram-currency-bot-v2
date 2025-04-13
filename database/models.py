"""
Database models and table creation for the Telegram Currency Bot.

This module defines the database schema and provides a function to create necessary tables.

Functions:
    create_tables: Creates the required database tables if they do not already exist.
"""

import aiosqlite
from utils.config import Config
from utils.logger import get_logger

# Path to the SQLite database file
DB_PATH = Config.DB_PATH

# Initialize logger for this module
logger = get_logger("DatabaseModels")


async def create_tables():
    """
    Creates the necessary database tables if they do not already exist.

    Tables:
        - api_rates: Stores official currency rates.
        - sharaf_exchange_rates: Stores exchange rates from Sharaf Exchange.
    """
    try:
        logger.info("Creating database tables if they do not exist.")
        async with aiosqlite.connect(DB_PATH) as conn:
            # Table for storing official API currency rates
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS api_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_code TEXT NOT NULL UNIQUE,
                usd_to_currency REAL,
                euro_to_currency REAL,
                date TIMESTAMP
            );
            """)

            # Index for faster lookups on currency_code in api_rates
            await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_api_currency_code ON api_rates(currency_code);
            """)

            # Table for storing Sharaf Exchange currency rates
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS sharaf_exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_code TEXT NOT NULL UNIQUE,
                buy_aed REAL,
                sell_aed REAL,
                date TIMESTAMP
            );
            """)

            # Index for faster lookups on currency_code in sharaf_exchange_rates
            await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sharaf_currency_code ON sharaf_exchange_rates(currency_code);
            """)

            # Commit the changes to the database
            await conn.commit()
            logger.info("Database tables created successfully.")
    except Exception as e:
        # Log any errors that occur during table creation
        logger.error(f"Error in create_tables: {e}", exc_info=True)
