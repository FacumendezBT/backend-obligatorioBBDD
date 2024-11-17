import mysql.connector
from config.logger import db_logger as logger
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorBufferedDict
from config import db_config


class ConnectionSingleton:
    cnx: MySQLConnection
    cursor: MySQLCursorBufferedDict
    msg: str

    this: object = None

    def __init__(self) -> None:
        try:
            self.cnx = mysql.connector.connect(
                user=db_config.USER_BD,
                password=db_config.PASSWD_BD,
                host=db_config.HOST_BD,
                database=db_config.DB_NAME,
            )
            self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
        except mysql.connector.Error as err:
            self.msg = err
            logger.error(err)
        else:
            self.msg = "OK"

    @classmethod
    def get_instance(cls) -> object:
        if not cls.this:
            cls.this = cls()

        return cls.this

    def disconnect(self) -> None:
        self.cursor.close()
        self.cnx.close()

    def _execute(self, query: str, values: dict | None) -> bool:
        try:
            if values:
                logger.info(f"Executing query: {query} with values: {values}")
                self.cursor.execute(query, values)
            else:
                logger.info(f"Executing query: {query}")
                self.cursor.execute(query)
        except mysql.connector.Error as err:
            self.msg = err
            self.cnx.rollback()
            logger.error(err)
            return False
        else:
            logger.info("Query executed successfully")
            self.cnx.commit()
            return True

    def get_all(self, table: str) -> dict | None:
        query = f"SELECT * FROM {table}"

        if not self._execute(query, None):
            return None

        return self.cursor.fetchall()

    def get_all_with(self, table: str, attributes: dict) -> dict | None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in attributes.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {condition_placeholder}"

        if not self._execute(query, attributes):
            return None

        return self.cursor.fetchall()

    def get_row(self, table, prim_keys: dict) -> dict | None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {condition_placeholder}"

        if not self._execute(query, prim_keys):
            return None

        return self.cursor.fetchone()

    def insert_row(self, table, row: dict) -> bool:
        # Docs: https://dev.mysql.com/doc/connector-python/
        # en/connector-python-example-cursor-transaction.html
        columns = ", ".join(list(row.keys()))
        placeholder = ", ".join([f"%({key})s" for key in row.keys()])

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholder})"

        if not self._execute(query, row):
            return False

        return True

    def update_row(self, table, new_attributes: dict, prim_keys: dict) -> bool:
        placeholder = ", ".join([f"{key}=%({key})s" for key in new_attributes.keys()])
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )

        query = f"UPDATE {table} SET {placeholder} WHERE {condition_placeholder}"

        if not self._execute(query, {**new_attributes, **prim_keys}):
            return False

        return True

    def delete_row(self, table, prim_keys: dict) -> None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )

        query = f"DELETE FROM {table} WHERE ({condition_placeholder})"

        if not self._execute(query, prim_keys):
            return False

        return True
