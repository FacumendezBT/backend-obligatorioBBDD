from datetime import date

"""
Description: This class represents a tuple of the alumno(...) table in the database.
"""


class Alumno:
    def __init__(
        self: object,
        ci: int,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono_contacto: int,
        correo_electronico: str,
    ) -> None:
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono_contacto = telefono_contacto
        self.correo_electronico = correo_electronico

    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj(
            result_row["ci"],
            result_row["nombre"],
            result_row["apellido"],
            result_row["fecha_nacimiento"],
            result_row["telefono_contacto"],
            result_row["correo_electronico"],
        )
