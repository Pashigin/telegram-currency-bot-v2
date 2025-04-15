# Telegram Currency Bot

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

Telegram Currency Bot is a robust, real-time currency exchange rate tracking solution delivered via the Telegram platform. The bot aggregates data from multiple authoritative sources including official exchange rates and commercial exchange services such as Sharaf Exchange, providing users with comprehensive and up-to-date currency information.

## Key Features

- **Multi-source Data Collection**: Obtain exchange rates from official banking sources
- **Commercial Exchange Monitoring**: Track rates from Sharaf Exchange and other services
- **Interactive Interface**: User-friendly experience with intuitive Telegram inline buttons
- **Scheduled Updates**: Automatic data refreshes to ensure information accuracy
- **SQLite Database**: Efficient local storage of exchange rate history

## Technical Requirements

- Python 3.12 or higher
- Telegram Bot API access
- Internet connection for data collection

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/telegram-currency-bot.git
   cd telegram-currency-bot
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   LOG_LEVEL=INFO  # Optional: DEBUG, INFO, WARNING, ERROR, CRITICAL
   ```

5. **Initialize the database**:
   ```bash
   python -m database.db_utils
   ```

6. **Launch the bot**:
   ```bash
   python main.py
   ```

## Project Architecture

```
telegram-currency-bot/
├── bot/                # Telegram bot core functionality
│   ├── config/         # Bot configuration and initialization
│   └── handlers/       # Command and callback handlers
├── collectors/         # Data collection modules
│   ├── api_collector.py      # API-based data retrieval
│   └── scrapper_collector.py # Web scraping functionality
├── database/           # Data persistence layer
│   ├── models.py       # SQLite database models
│   └── db_utils.py     # Database utility functions
├── jobs/               # Scheduled background tasks
├── utils/              # Helper utilities
│   ├── config.py       # Configuration management
│   ├── formatters.py   # Data formatting utilities
│   └── logger.py       # Logging configuration
└── main.py             # Application entry point
```

## Docker Deployment

A Dockerfile is included for containerized deployment:

```bash
docker build -t telegram-currency-bot .
docker run -d --name currency-bot --env-file .env telegram-currency-bot
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.