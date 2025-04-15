# db_helpers.py
"""
Database helper functions module.

This module provides reusable database operations such as updating and fetching data.

Functions:
    update_rates: Inserts or updates rates in a specified table.
    fetch_rates: Fetches data from a table based on a condition.
"""

import aiosqlite
from utils.config import Config
from utils.logger import get_logger

# Path to the SQLite database file
DB_PATH = Config.DB_PATH

# Initialize logger for this module
logger = get_logger(__name__)


async def update_rates(table_name, columns, data):
    """
    Inserts or updates rates in a specified table using the ON CONFLICT clause.

    Args:
        table_name (str): The name of the database table.
        columns (list): A list of column names for the table.
        data (list of tuples): The data to be inserted or updated.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            # Prepare placeholders and update clause for the SQL query
            placeholders = ", ".join(["?" for _ in columns])
            update_clause = ", ".join(
                [f"{col} = excluded.{col}" for col in columns[1:]]
            )

            # Execute the SQL query to insert or update data
            await conn.executemany(
                f"""
                INSERT INTO {table_name} ({", ".join(columns)})
                VALUES ({placeholders})
                ON CONFLICT({columns[0]})
                DO UPDATE SET {update_clause}
                """,
                data,
            )
            await conn.commit()

        logger.info(f"Updated {table_name} with {len(data)} entries.")
    except Exception as e:
        # Log any errors that occur during the update operation
        logger.error(f"Failed to update rates in {table_name}: {e}", exc_info=True)


async def fetch_rates(table_name, columns, condition_column, condition_value):
    """
    Fetches data from a table based on a condition.

    Args:
        table_name (str): The name of the database table.
        columns (list): A list of column names to fetch.
        condition_column (str): The column name for the condition.
        condition_value: The value to match in the condition column.

    Returns:
        tuple: The fetched row from the database, or None if no match is found.
    """
    async with aiosqlite.connect(DB_PATH) as conn:
        # Prepare the SQL query to fetch data
        query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {condition_column} = ?"

        async with conn.execute(query, (condition_value,)) as cursor:
            result = await cursor.fetchone()

            # Log at debug level instead of info to reduce log noise
            logger.debug(
                f"Fetched data for condition: {condition_column} = {condition_value}, Result: {result}"
            )

            return result
