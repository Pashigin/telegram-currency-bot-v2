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
