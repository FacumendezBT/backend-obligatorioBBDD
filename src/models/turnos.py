from datetime import time

"""
Description: This class represents a tuple of the turnos(...) table in the database.
"""


class Turnos:
    def __init__(self: object, id: int, starting_time: time, ending_time: time) -> None:
        self.id = id
        self.hora_inicio = starting_time
        self.hora_fin = ending_time

    @classmethod
    def map_result(obj: object, result_row: dict) -> object:
        return obj(result_row["id"], result_row["hora_inicio"], result_row["hora_fin"])
