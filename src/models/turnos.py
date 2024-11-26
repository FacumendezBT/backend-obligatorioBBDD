from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection
from datetime import time
from utils.time import convertir_a_time


class Turnos(GenericModel):
    table: str = "turnos"
    id: int
    hora_inicio: time
    hora_fin: time
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
        }

    def __init__(
        self, id: int, hora_inicio: time, hora_fin: time, is_new: bool
    ) -> None:
        self.id = id
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("id"),
            request_data.get("hora_inicio"),
            request_data.get("hora_fin"),
            is_new,
        )

    @classmethod
    def get_all(cls) -> list[object]:
        db = DatabaseConnection()
        result = db.get_all(cls.table)

        if not result:
            return []

        return [
            cls(
                row["id"],
                row["hora_inicio"],
                row["hora_fin"],
                False,
            )
            for row in result
        ]

    @classmethod
    def get_row(cls, prim_keys: dict) -> object | None:
        db = DatabaseConnection()
        result = db.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(
            result["id"],
            result["hora_inicio"],
            result["hora_fin"],
            False,
        )

    def save(self) -> bool:
        self.hora_inicio = convertir_a_time(self.hora_inicio)
        self.hora_fin = convertir_a_time(self.hora_fin)
        # Validaciones básicas
        if (
            not isinstance(self.hora_inicio, time)
            or not isinstance(self.hora_fin, time)
        ):
            print("ACA")
            return False

        db = DatabaseConnection()

        if self.is_new:
            success = db.insert_row(
                self.table,
                self.to_dict(),
            )
        else:
            if not isinstance(self.id, int):
                print("ACA2")
                return False

            success = db.update_row(
                self.table,
                self.to_dict(),
                {"id": self.id},
            )
        return success

    def delete_self(self) -> bool:
        db = DatabaseConnection()
        success = db.delete_row(self.table, {"id": self.id})
        if success:
            self.id = None
            self.hora_inicio = None
            self.hora_fin = None
        return success
