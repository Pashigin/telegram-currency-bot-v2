from bot.config import bot, create_markup
from database.db_utils import fetch_api_rates, fetch_scrapper_rates

markup = create_markup()


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для получения курсов валют. Вот доступные команды:",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Проверить оф. курсы валют")
def get_api_rates(message):
    rates = fetch_api_rates("AED")

    if rates:
        try:
            usd_to_aed = rates[1]
            eur_to_aed = rates[2]

            response = (
                "📊 Официальные курсы валют на сегодня:\n\n"
                f"💵 1 USD = {usd_to_aed:.4f} AED\n"
                f"💶 1 EUR = {eur_to_aed:.4f} AED"
            )
        except (ValueError, TypeError) as e:
            response = f"⚠️ Произошла ошибка при обработке данных курсов валют. {e}"
    else:
        response = "❌ Не удалось получить официальные курсы валют. Попробуйте позже."

    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(
    func=lambda message: message.text == "Проверить курс обменника Sharaf Exchange"
)
def get_scrapper_rates(message):
    usd_rate = fetch_scrapper_rates("USD")
    eur_rate = fetch_scrapper_rates("EUR")

    if usd_rate and eur_rate:
        try:
            usd_buy = usd_rate[1]
            usd_sell = usd_rate[2]

            eur_buy = eur_rate[1]
            eur_sell = eur_rate[2]

            response = (
                "📊 Курсы обменника на сегодня:\n\n"
                "Покупают:\n"
                f"💵 1 USD = {usd_buy:.4f} AED\n"
                f"💶 1 EUR = {eur_buy:.4f} AED\n\n"
                "Продают:\n"
                f"💵 1 USD = {usd_sell:.4f} AED\n"
                f"💶 1 EUR = {eur_sell:.4f} AED"
            )
        except (ValueError, TypeError) as e:
            print(f"Error processing scrapper rates: {e}")
            response = "⚠️ Произошла ошибка при обработке данных курсов обменника"
    else:
        response = "❌ Не удалось получить курсы обменника. Попробуйте позже."

    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(func=lambda message: message.text == "Помощь")
def send_help(message):
    help_text = (
        "💡 Этот бот позволяет вам получать актуальные курсы валют для Дирхама ОАЭ (AED).\n\n"
        "Вы можете использовать следующие команды:\n"
        "- Проверить оф. курсы валют\n"
        "- Проверить курс обменника Sharaf Exchange\n"
        "- Для связи @pashigin\n\n"
    )
    bot.send_message(chat_id=message.chat.id, text=help_text)


if __name__ == "__main__":
    bot.polling()
