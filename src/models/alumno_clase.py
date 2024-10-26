"""
Description: This class represents a tuple of the alumno_clase(...) table in the database.
"""


class AlumnoClase:
    def __init__(self: object, id_clase: int, ci_alumno: int, id_equipamiento: int) -> None:
        self.id_clase = id_clase
        self.ci_alumno = ci_alumno
        self.id_equipamiento = id_equipamiento

    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj(
            result_row["id_clase"],
            result_row["ci_alumno"],
            result_row["id_equipamiento"],
        )
