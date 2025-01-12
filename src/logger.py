import logging
import sqlite3
from datetime import datetime

logging.basicConfig(
    encoding = 'utf-8',
    level = logging.DEBUG,
    format = '%(asctime)s-%(levelname)s-%(name)s-%(message)s',
    datefmt = "%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger('TaskAPI')
log.setLevel(logging.DEBUG)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)
console_logger.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(name)s-%(message)s"))

class Sql_Handler(logging.Handler):
    def __init__(self, db_path):
        super().__init__()
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS app_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                level TEXT,
                message TEXT
                )
                """
            )
    def emit(self, record):
        log_entry = self.format(record)
        timeStamp, level, message = log_entry.split(',',2)
        timeStamp = datetime.strptime(timeStamp, '%Y-%m-%d %H:%M:%S')
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO app_logs(timestamp, level, message) VALUES(?,?,?)
                """,
                (timeStamp, level, message)
            )
    def close(self):
        self.connection.close()
        super().close()

sql_handler = Sql_Handler('log.db')
sql_handler.setLevel(logging.DEBUG)
sql_handler.setFormatter(logging.Formatter("%(asctime)s, %(levelname)s, %(message)s"))

log.addHandler(console_logger)
log.addHandler(sql_handler)
