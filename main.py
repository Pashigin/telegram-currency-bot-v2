import asyncio
from bot.handlers.commands import bot

if __name__ == "__main__":
    asyncio.run(bot.polling())
