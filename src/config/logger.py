import logging

# Configuración del logger para la aplicación
app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.INFO)

app_handler = logging.FileHandler("app.log")
app_handler.setLevel(logging.INFO)

app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)

app_logger.addHandler(app_handler)
app_logger.addHandler(logging.StreamHandler())

# Configuración del logger para la base de datos
db_logger = logging.getLogger("db_logger")
db_logger.setLevel(logging.INFO)

db_handler = logging.FileHandler("database.log")
db_handler.setLevel(logging.INFO)

db_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db_handler.setFormatter(db_formatter)

db_logger.addHandler(db_handler)
db_logger.addHandler(logging.StreamHandler())