import sqlite3


def create_tables(db_path="data/currency_data.sqlite"):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Таблица для API
        cur.execute("""
        CREATE TABLE IF NOT EXISTS api_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT NOT NULL UNIQUE,
            usd_to_currency REAL,
            euro_to_currency REAL,
            date TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_currency_code ON api_rates(currency_code);
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sharaf_exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT NOT NULL UNIQUE,
            buy_aed REAL,
            sell_aed REAL,
            date TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_currency_code ON sharaf_exchange_rates(currency_code);
        """)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_tables()
