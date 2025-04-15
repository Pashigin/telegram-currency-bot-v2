"""
Jobs package for scheduled tasks.

This package contains modules for scheduled and recurring tasks in the currency bot.
"""

from utils.logger import get_logger
from .daily_job import daily_job

logger = get_logger(__name__)

__all__ = ["daily_job"]
