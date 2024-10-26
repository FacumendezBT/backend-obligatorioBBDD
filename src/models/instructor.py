"""
Description: This class represents a tuple of the instructor(...) table in the database.
"""


class Instructor:
    def __init__(self: object, ci: int, nombre: str, apellido: str) -> None:
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido

    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj(result_row["ci"], result_row["nombre"], result_row["apellido"])
