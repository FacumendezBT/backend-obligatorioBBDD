import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorBufferedDict
from src.config import db_config


class GenericModel:
    table: str  # Cada model hace override
    msg: str  # Acá vamos a guardar los mesajes de error que nos tire el motor
    cnx: MySQLConnection  # Representa una conexión a una base de datos
    cursor: MySQLCursorBufferedDict  # Para ejecutar operaciones en la bd

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
        else:
            self.msg = "OK"

    # Cortamos la conexión cuando se va del scope
    # ...o cuando se le cante al garbage collector
    # Si hay drama podemos cambiar a un context manager
    def __del__(self) -> None:
        self.cursor.close()
        self.cnx.close()

    # Estos métodos tienen bastante funcionalidad implementada. La idea es que
    # cada clase haga override para agregar la funcionalidad necesaria y luego
    # llamen al método correspondiente de la clase base.

    def get_row(self, prim_keys: dict) -> None:
        condition_placeholder = " AND ".join(
            [f"{key} = %s" for key in prim_keys.keys()]
        )
        query = f"SELECT * FROM {self.table} WHERE {condition_placeholder}"

        try:
            self.cursor.execute(query, tuple(prim_keys.values()))
        except mysql.connector.Error as err:
            self.msg = err
        else:
            self.msg = "OK"

        # Cada clase toma el dicc de respuesta y hace las asignaciones
        # correspondientes.

    def insert_row(self, row: dict) -> bool:
        # Docs: https://dev.mysql.com/doc/connector-python/
        # en/connector-python-example-cursor-transaction.html
        columns = ", ".join(list(row.keys()))
        placeholder = ", ".join([f"%({key})s" for key in row.keys()])

        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholder})"

        try:
            self.cursor.execute(query, row)
        except mysql.connector.Error as err:
            self.msg = err
            self.cnx.rollback()
            return False
        else:
            self.cnx.commit()
            return True

    def update_row(self, new_attributes: dict, condition: dict) -> None:
        pass

    def delete_row(self, condition: dict) -> None:
        pass
