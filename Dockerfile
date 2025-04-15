# Легковесный образ Python
FROM python:3.12-slim

# Установка Playwright и Chromium
RUN pip install --no-cache-dir playwright \
    && playwright install --with-deps --only-shell chromium  

# Создание рабочей директории
WORKDIR /app

# Копирование всего проекта
COPY . /app/

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Добавление cron-задания для daily_job.py каждую минуту (для тестирования)
RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && echo "* 4 * * * cd /app && PYTHONPATH=/app /usr/local/bin/python /app/jobs/daily_job.py >> /var/log/cron.log 2>&1" > /etc/cron.d/daily_job \
    && chmod 0644 /etc/cron.d/daily_job \
    && crontab /etc/cron.d/daily_job \
    && touch /var/log/cron.log \
    && rm -rf /var/lib/apt/lists/*

# Создание стартового скрипта
RUN echo '#!/bin/sh\nservice cron start\necho "Cron service started"\npython /app/main.py' > /app/start.sh \
    && chmod +x /app/start.sh

# Команда для запуска скрипта
CMD ["/app/start.sh"]