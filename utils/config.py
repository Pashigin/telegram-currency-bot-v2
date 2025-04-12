import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_TOKEN_TEST = os.getenv("TELEGRAM_TOKEN_TEST")
    DB_PATH = os.getenv("DB_PATH", "data/currency_data.sqlite")
    API_USD_URL = os.getenv("API_USD_URL", "https://open.er-api.com/v6/latest/USD")
    API_EUR_URL = os.getenv("API_EUR_URL", "https://open.er-api.com/v6/latest/EUR")
    SCRAPPER_URL = os.getenv(
        "SCRAPPER_URL", "https://www.sharafexchange.ae/services/currency-exchange"
    )
