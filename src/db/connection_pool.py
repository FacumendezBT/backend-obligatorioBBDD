import mysql.connector.pooling
from config.logger import db_logger as logger
from config import db_config

class ConnectionPool:
    _pool = None

    @classmethod
    def shutdown(cls):
        if cls._pool:
            cls._pool.close()
            logger.info("Pool de conexiones cerrado, a ver si con esto malloc no llora.")

    @classmethod
    def init(cls):
        try:
            cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="malloc_de_esta_no_te_librás",
                pool_size=5,
                pool_reset_session=True,
                user=db_config.USER_BD,
                password=db_config.PASSWD_BD,
                host=db_config.HOST_BD,
                database=db_config.DB_NAME,
            )
            logger.info("Pool de conexiones iniciado, malloc contentísimo.")
        except mysql.connector.Error as err:
            logger.error(f"Error al inicializar el pool de conexiones: {err}")

    @classmethod
    def get_connection(cls):
        try:
            cnx = cls._pool.get_connection()
            logger.info("Conexión obtenida del pool.")
            return cnx
        except mysql.connector.Error as err:
            logger.error(f"Error al obtener conexión del pool: {err}")
            return None
