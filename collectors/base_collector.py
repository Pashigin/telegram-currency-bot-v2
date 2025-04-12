from abc import ABC, abstractmethod
from collections.abc import Coroutine


class BaseCollector(ABC):
    """Базовый интерфейс для всех сборщиков данных."""

    @abstractmethod
    def collect_data(self) -> Coroutine:
        """Метод для сбора данных."""
        pass
