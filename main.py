"""
Entry point for the Telegram Currency Bot.

This script initializes the bot and starts polling for messages.
"""

import asyncio
import sys
from utils.logger import get_logger
from bot.handlers.commands import bot
from database.models import create_tables

# Initialize logger for the main script
logger = get_logger("Main")

if __name__ == "__main__":
    try:
        # Log the start of the bot and database initialization
        logger.info("Starting the bot and initializing database tables.")

        # Create database tables asynchronously
        asyncio.run(create_tables())
        logger.info("Database tables initialized. Starting bot polling.")

        # Start polling for bot commands
        asyncio.run(bot.polling())
    except Exception as e:
        # Log any errors that occur during execution
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
