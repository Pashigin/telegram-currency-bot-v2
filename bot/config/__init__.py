"""
Configuration and initialization for the Telegram bot.

This module sets up the bot instance and provides utility functions like creating a keyboard markup.
"""

from telebot.async_telebot import AsyncTeleBot
from telebot import types
from utils.config import Config

TELEGRAM_TOKEN = Config.TELEGRAM_TOKEN_TEST

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN can not be None")

bot = AsyncTeleBot(TELEGRAM_TOKEN)


def create_markup():
    """
    Creates a keyboard markup for the bot's interface.

    Returns:
        types.ReplyKeyboardMarkup: A keyboard markup with predefined buttons.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Проверить оф. курсы валют"))
    markup.add(
        types.KeyboardButton("Проверить курс обменника Sharaf Exchange"),
    )
    markup.add(
        types.KeyboardButton("Здесь может быть ваша реклама"),
        types.KeyboardButton("Помощь"),
    )
    return markup
