from datetime import date

"""
Description: This class represents a tuple of the equipamiento(...) table in the database.
"""


class Clase:
    def __init__(
        self: object,
        id: int,
        ci_instructor: int,
        id_actividad: int,
        id_turno: int,
        dictada: bool,
        fecha: date,
    ) -> None:
        self.id = id
        self.ci_instructor = ci_instructor
        self.id_actividad = id_actividad
        self.id_turno = id_turno
        self.dictada = dictada
        self.fecha = fecha


    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj (
            result_row["id"],
            result_row["ci_instructor"],
            result_row["id_actividad"],
            result_row["id_turno"],
            result_row["dictada"],
            result_row["fecha"],
        )
