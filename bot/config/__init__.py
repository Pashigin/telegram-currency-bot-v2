from telebot import TeleBot, types
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_TEST")

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN can not be None")

bot = TeleBot(TELEGRAM_TOKEN)


def create_markup():
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
