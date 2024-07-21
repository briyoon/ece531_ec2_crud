import sqlite3
from contextlib import contextmanager
import logging
import logging.handlers

logger = logging.getLogger("ModelLogger")
logger.setLevel(logging.ERROR)

syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
syslog_handler.setFormatter(formatter)

logger.addHandler(syslog_handler)


@contextmanager
def get_db_connection():
    connection = sqlite3.connect("sqlite3.db", check_same_thread=False)
    try:
        yield connection
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        connection.close()


class Model:
    def __init__(self):
        with get_db_connection() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    item TEXT NOT NULL
                )
                """
            )
            db.commit()

    def create_item(self, item: str):
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO items (item) VALUES (?)", (item,))
            db.commit()
            return cursor.lastrowid

    def get_item(self, id: int):
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT item FROM items WHERE id = ?", (id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_all_items(self):
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM items")
            return cursor.fetchall()

    def update_item(self, id: int, item: str):
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("UPDATE items SET item = ? WHERE id = ?", (item, id))
            db.commit()
            return cursor.rowcount > 0

    def delete_item(self, id: int):
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM items WHERE id = ?", (id,))
            db.commit()
            return cursor.rowcount > 0
