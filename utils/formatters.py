"""
This module contains formatting functions for currency responses and error messages.

Functions:
    format_api_currency_response: Formats the currency response for API rates.
    format_scrapper_currency_response: Formats the currency response for scrapper rates.
    format_check_currency_response: Formats the response for the /check command.
    format_help_message: Returns a help message for the bot.
    format_error_message: Formats an error message for the bot.
"""

# This module contains formatting functions for currency responses.


def format_api_currency_response(rates):
    """
    Formats the currency response for API rates.

    Args:
        rates (tuple): A tuple containing currency code, USD rate, and EUR rate.

    Returns:
        str: A formatted string with the currency rates.
    """
    currency_code, usd_to_currency, eur_to_currency = rates
    return (
        f"📊 Официциальные курсы на сегодня:\n\n"
        f"💵 1 USD = {usd_to_currency:.4f} {currency_code}\n"
        f"💶 1 EUR = {eur_to_currency:.4f} {currency_code}"
    )


def format_scrapper_currency_response(usd_rate, eur_rate):
    """
    Formats the currency response for scrapper rates.

    Args:
        usd_rate (tuple): A tuple containing currency code, buy AED rate, and sell AED rate for USD.
        eur_rate (tuple): A tuple containing currency code, buy AED rate, and sell AED rate for EUR.

    Returns:
        str: A formatted string with the scrapper rates.
    """
    usd_currency_code, usd_buy, usd_sell = usd_rate
    eur_currency_code, eur_buy, eur_sell = eur_rate
    return (
        "📊 Курсы обменника на сегодня:\n\n"
        "Покупают:\n"
        f"💵 1 USD = {usd_buy:.4f} AED\n"
        f"💶 1 EUR = {eur_buy:.4f} AED\n\n"
        "Продают:\n"
        f"💵 1 USD = {usd_sell:.4f} AED\n"
        f"💶 1 EUR = {eur_sell:.4f} AED"
    )


def format_check_currency_response(
    currency_code, api_usd_rate, api_eur_rate, scrapper_rate
):
    """
    Форматирует ответ для команды /check.
    """
    api_usd_response = (
        f"1 USD = {api_usd_rate[1]:.4f} {currency_code}"
        if isinstance(api_usd_rate, tuple) and api_usd_rate[1]
        else f"1 USD = Не найдено {currency_code}"
    )
    api_eur_response = (
        f"1 EUR = {api_eur_rate[2]:.4f} {currency_code}"
        if isinstance(api_eur_rate, tuple) and api_eur_rate[2]
        else f"1 EUR = Не найдено {currency_code}"
    )

    scrapper_response = ""
    if scrapper_rate and all(scrapper_rate):
        scrapper_buy, scrapper_sell = scrapper_rate
        scrapper_response = (
            f"1 {currency_code} = {scrapper_buy:.4f} AED (покупка)\n"
            f"1 {currency_code} = {scrapper_sell:.4f} AED (продажа)"
        )

    return f"Официальный курс:\n{api_usd_response}\n{api_eur_response}\n\n" + (
        f"Курс Обменника:\n{scrapper_response}" if scrapper_response else ""
    )


def format_help_message():
    """
    Returns a help message for the bot.
    This message provides information about the bot's functionality and available commands.
    Returns:
        str: A formatted help message.
    """
    return (
        "💡 Этот бот позволяет вам получать актуальные курсы валют для Дирхама ОАЭ (AED).\n\n"
        "Вы можете использовать следующие команды:\n"
        "- Проверить оф. курсы валют (/check_rates)\n"
        "- Проверить курс обменника Sharaf Exchange (/check_exchange)\n"
        "- Помощь (/help)\n"
        "- Для связи @pashigin\n\n"
    )
