"""
Main entry point for Telegram Currency Bot.

This script initializes the Telegram bot for retrieving currency rates,
creates the necessary database tables, and starts the process
of listening for user messages.
"""

import asyncio
import sys
from bot.handlers.commands import bot
from database.models import create_tables
from utils.logger import get_logger

# Initialize logger for the main script
logger = get_logger(__name__)


async def start_bot():
    """
    Initializes the database and starts the bot's polling.
    """
    try:
        # Log the start of the bot and database initialization
        logger.info("Starting the bot and initializing database tables.")

        # Create database tables
        await create_tables()
        logger.info("Database tables initialized. Starting bot polling.")

        # Start polling for bot commands with safe timeouts
        await bot.infinity_polling(
            timeout=10,  # timeout между запросами
            request_timeout=35,  # общий таймаут запроса
        )
    except Exception as e:
        # Log any errors that occur during execution
        logger.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
        sys.exit(0)
