# Telegram Currency Bot

## Description
Telegram Currency Bot is a tool for tracking currency exchange rates. It provides up-to-date exchange rate data from official sources and exchange services like Sharaf Exchange.

## Features
- Retrieve official currency exchange rates.
- Fetch exchange rates from Sharaf Exchange.
- User-friendly interface with interactive buttons.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone <URL>
   cd telegram-currency-bot
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add the required environment variables:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   ```

4. Start the bot:
   ```bash
   python main.py
   ```

## Project Structure
- `main.py` — Entry point for running the bot.
- `bot/` — Telegram command handlers.
  - `config/` — Bot configuration and initialization.
  - `handlers/` — Command handlers.
- `collectors/` — Modules for data collection.
  - `api_collector.py` — Collect data via APIs.
  - `scrapper_collector.py` — Collect data via web scraping.
- `database/` — Database management.
  - `models.py` — Database table definitions.
  - `db_utils.py` — Utilities for database operations.
- `jobs/` — Scheduled tasks.
- `utils/` — Utility modules.
  - `config.py` — Project configuration.
  - `logger.py` — Logging setup.

## Usage Example
After starting the bot, use one of the available commands:
- `/start` — Begin interacting with the bot.
- `/help` — Get a list of available commands.
- Use the interactive buttons to fetch currency exchange rates.

## License
This project is licensed under the MIT License.