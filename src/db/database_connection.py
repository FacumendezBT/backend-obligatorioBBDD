from db import ConnectionPool
from config.logger import db_logger as logger
import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.cnx = ConnectionPool.get_connection()
        if self.cnx:
            self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
            self.msg = "OK"
        else:
            self.cursor = None
            self.msg = "Error al obtener la conexión, ay"
            logger.error(self.msg)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
            logger.info("Cursor cerrado.")
        if self.cnx:
            self.cnx.close()
            logger.info("Conexión devuelta al pool, malloc feliz.")

    def _execute(self, query: str, values: dict | None) -> bool:
        try:
            if not self.cursor:
                logger.error("No hay cursor disponible para ejecutar la consulta, así son")
                return False
            if values:
                logger.info(f"Ejecutando consulta: {query} con valores: {values}")
                self.cursor.execute(query, values)
            else:
                logger.info(f"Ejecutando consulta: {query}")
                self.cursor.execute(query)
            self.cnx.commit()
            logger.info("Consulta ejecutada y cambios confirmados, que buen año")
            return True
        except mysql.connector.Error as err:
            self.cnx.rollback()
            logger.error(f"Error al ejecutar la consulta: {err}", exc_info=True)
            return False

    def get_all(self, table: str) -> list[dict] | None:
        query = f"SELECT * FROM {table}"
        if not self._execute(query, None):
            self.disconnect()
            return None
        results = self.cursor.fetchall()
        logger.info(f"Resultados obtenidos: {results}")
        self.disconnect()
        return results

    def get_all_with(self, table: str, attributes: dict) -> list[dict] | None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in attributes.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {condition_placeholder}"
        if not self._execute(query, attributes):
            self.disconnect()
            return None
        results = self.cursor.fetchall()
        logger.info(f"Resultados obtenidos: {results}")
        self.disconnect()
        return results

    def get_row(self, table: str, prim_keys: dict) -> dict | None:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )
        query = f"SELECT * FROM {table} WHERE {condition_placeholder}"
        if not self._execute(query, prim_keys):
            self.disconnect()
            return None
        result = self.cursor.fetchone()
        logger.info(f"Resultado obtenido: {result}")
        self.disconnect()
        return result

    def insert_row(self, table: str, row: dict) -> bool:
        columns = ", ".join(row.keys())
        placeholders = ", ".join([f"%({key})s" for key in row.keys()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        success = self._execute(query, row)
        self.disconnect()
        return success

    def update_row(self, table: str, new_attributes: dict, prim_keys: dict) -> bool:
        set_placeholder = ", ".join([f"{key} = %({key})s" for key in new_attributes.keys()])
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )
        query = f"UPDATE {table} SET {set_placeholder} WHERE {condition_placeholder}"
        params = {**new_attributes, **prim_keys}
        success = self._execute(query, params)
        self.disconnect()
        return success

    def delete_row(self, table: str, prim_keys: dict) -> bool:
        condition_placeholder = " AND ".join(
            [f"{key} = %({key})s" for key in prim_keys.keys()]
        )
        query = f"DELETE FROM {table} WHERE {condition_placeholder}"
        success = self._execute(query, prim_keys)
        self.disconnect()
        return success