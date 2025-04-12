# Telegram Currency Bot

## Описание
Бот для отслеживания курсов валют с использованием Telegram.

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <URL>
   cd telegram-currency-bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корне проекта и добавьте переменные окружения:
   ```env
   TELEGRAM_TOKEN=ваш_токен
   DATABASE_URL=sqlite:///data/currency_data.sqlite
   ```

4. Запустите бота:
   ```bash
   python main.py
   ```

## Тестирование

1. Установите зависимости для тестирования:
   ```bash
   pip install pytest
   ```

2. Запустите тесты:
   ```bash
   pytest
   ```

## Структура проекта
- `bot/` - обработчики команд Telegram.
- `collectors/` - модули для сбора данных.
- `database/` - работа с базой данных.
- `jobs/` - периодические задачи.
- `services/` - бизнес-логика.
- `utils/` - вспомогательные модули.