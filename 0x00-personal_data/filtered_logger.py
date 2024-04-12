#!/usr/bin/env python3
"""Defining a Function filter_datum"""
from typing import List, Tuple
import re
import logging
import mysql.connector
from os import getenv
import mysql.connector


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = '|'.join(fields)
    return re.sub(f'({pattern})=([^{separator}]+)',
                  f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes new formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns a str representation of a LogRecord"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    user_logger = logging.getLogger('user_data')
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False
    user_logger.addHandler(handler)
    return user_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = getenv('PERSONAL_DATA_DB_NAME')
    db_connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    return db_connection


def main():
    """displays the logs info in from the database"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        user_data_str = (
            f'name={row[0]}; '
            f'email={row[1]}; '
            f'phone={row[2]}; '
            f'ssn={row[3]}; '
            f'password={row[4]}; '
            f'ip={row[5]}; '
            f'last_login={row[6]}; '
            f'user_agent={row[7]};'
        )
        logger.info(user_data_str)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
