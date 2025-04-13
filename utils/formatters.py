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


def format_check_currency_response(currency_code, api_rate, scrapper_rate):
    """
    Formats the response for the /check command.

    Args:
        currency_code (str): The currency code being checked.
        api_rate (tuple or None): A tuple containing API rates (currency_code, USD rate, EUR rate) or None.
        scrapper_rate (tuple or None): A tuple containing scrapper rates (buy AED rate, sell AED rate) or None.

    Returns:
        str: A formatted response string.
    """

    # Format API rates
    if api_rate:
        usd_api, eur_api = api_rate
        api_response = (
            f"💵 1 USD = {usd_api:.4f} {currency_code}\n"
            f"💶 1 EUR = {eur_api:.4f} {currency_code}"
        )
    else:
        api_response = "Не найдены."

    # Format scrapper rates
    if scrapper_rate:
        scrapper_buy, scrapper_sell = scrapper_rate
        scrapper_response = (
            f"1 {currency_code} = {scrapper_buy:.4f} AED (покупка)\n"
            f"1 {currency_code} = {scrapper_sell:.4f} AED (продажа)"
        )
    else:
        scrapper_response = "Не найдены."

    return f"📊 Официальный курс:\n{api_response}\n\n📊 Курс Обменника:\n{scrapper_response}"


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
        "/check_rates - Проверить оф. курсы валют\n"
        "/check_exchange - Проверить курс обменника Sharaf Exchange\n"
        "/check - Проверить определенную валюту (/check RUB)\n"
        "/update_rates - Обновить данные в базе\n"
        "/help - Помощь\n\n"
        "- Для связи @pashigin\n\n"
    )
