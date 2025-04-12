"""
Entry point for the Telegram Currency Bot.

This script initializes the bot and starts polling for messages.
"""

import asyncio

from bot.handlers.commands import bot

if __name__ == "__main__":
    asyncio.run(bot.polling())
