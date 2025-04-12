from bot.config import bot, create_markup
from database.db_utils import fetch_api_rates, fetch_scrapper_rates
import asyncio

markup = create_markup()


def format_currency_response(title, rates):
    try:
        usd_to_aed, eur_to_aed = rates
        return (
            f"📊 {title} на сегодня:\n\n"
            f"💵 1 USD = {usd_to_aed:.4f} AED\n"
            f"💶 1 EUR = {eur_to_aed:.4f} AED"
        )
    except (ValueError, TypeError) as e:
        return f"⚠️ Произошла ошибка при обработке данных курсов валют. {e}"


@bot.message_handler(commands=["start", "help"])
async def send_welcome(message):
    await bot.send_message(
        message.chat.id,
        "Привет! Я бот для получения курсов валют. Вот доступные команды:",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Проверить оф. курсы валют")
async def get_api_rates(message):
    rates = await fetch_api_rates("AED")

    if rates:
        response = format_currency_response("Официальные курсы валют", rates[1:])
    else:
        response = "❌ Не удалось получить официальные курсы валют. Попробуйте позже."

    await bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(
    func=lambda message: message.text == "Проверить курс обменника Sharaf Exchange"
)
async def get_scrapper_rates(message):
    usd_rate = await fetch_scrapper_rates("USD")
    eur_rate = await fetch_scrapper_rates("EUR")

    if usd_rate and eur_rate:
        try:
            response = (
                "📊 Курсы обменника на сегодня:\n\n"
                "Покупают:\n"
                f"💵 1 USD = {usd_rate[1]:.4f} AED\n"
                f"💶 1 EUR = {eur_rate[1]:.4f} AED\n\n"
                "Продают:\n"
                f"💵 1 USD = {usd_rate[2]:.4f} AED\n"
                f"💶 1 EUR = {eur_rate[2]:.4f} AED"
            )
        except (ValueError, TypeError) as e:
            print(f"Error processing scrapper rates: {e}")
            response = "⚠️ Произошла ошибка при обработке данных курсов обменника"
    else:
        response = "❌ Не удалось получить курсы обменника. Попробуйте позже."

    await bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(func=lambda message: message.text == "Помощь")
async def send_help(message):
    help_text = (
        "💡 Этот бот позволяет вам получать актуальные курсы валют для Дирхама ОАЭ (AED).\n\n"
        "Вы можете использовать следующие команды:\n"
        "- Проверить оф. курсы валют\n"
        "- Проверить курс обменника Sharaf Exchange\n"
        "- Для связи @pashigin\n\n"
    )
    await bot.send_message(chat_id=message.chat.id, text=help_text)


if __name__ == "__main__":
    asyncio.run(bot.polling())
