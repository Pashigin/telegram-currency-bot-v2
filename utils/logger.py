import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    """Возвращает настроенный логгер."""
    return logging.getLogger(name)
