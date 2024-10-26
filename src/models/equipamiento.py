"""
Description: This class represents a tuple of the equipamiento(...) table in the database.
"""


class Equipamiento:
    def __init__(self: object, id: int, id_actividad: int, descripcion: str, costo: int) -> None:
        self.id = id
        self.id_actividad = id_actividad
        self.descripcion = descripcion
        self.costo = costo

    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj(
            result_row["id"],
            result_row["id_actividad"],
            result_row["descripcion"],
            result_row["costo"],
        )
