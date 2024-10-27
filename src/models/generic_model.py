import mysql.connector
from src.config import db_config


class GenericModel:
    table = "" # Cada model hace override

    def __init__(self) -> None:
        try:
            self.cnx = mysql.connector.connect(
                user=db_config.USER_BD,
                password=db_config.PASSWD_BD,
                host=db_config.HOST_BD,
                database=db_config.DB_NAME,
            )
            self.cursor = self.cnx.cursor(dictionary=True)
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

    # Este método tiene bastante funcionalidad implementada. La idea es que
    # cada clase haga override para agregar los chequeos necesarios y luego
    # llamen al método del padre.
    def insert_row(self, row: dict) -> None:
        # Docs: https://dev.mysql.com/doc/connector-python/
        # en/connector-python-example-cursor-transaction.html
        columns = ", ".join(list(row.keys()))
        placeholder = ", ".join([f"%({key})s" for key in row.keys()])

        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholder})"

        try:
            self.cursor.execute(query, row)
        except mysql.connector.Error as err:
            self.msg = err
            self.cnx.rollback() # Si revienta cancelamos la transacción.
        else:
            self.cnx.commit()


    def update_row(self, new_attributes: dict) -> None:
        pass

    @classmethod
    def map_result(model: object, result_row: dict) -> None:
        pass
