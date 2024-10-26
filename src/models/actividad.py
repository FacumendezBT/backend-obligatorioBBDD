"""
Description: This class represents a tuple of the actividad(...) table in the database.
"""


class Actividad:
    def __init__(self: object, id: int, description: str, cost: int, age_restrict: int) -> None:
        self.id = id
        self.descripcion = description
        self.costo = cost
        self.restricion_edad = age_restrict

    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj(
            result_row["id"],
            result_row["descripcion"],
            result_row["costo"],
            result_row["restricion_edad"],
        )
