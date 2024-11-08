from fastapi import Request
from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton
from datetime import time


class Turnos(GenericModel):
    table: str = "turnos"
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
        self, id: int, starting_time: time, ending_time: time, is_new: bool
    ) -> None:
        super().__init__()
        self.id = id
        self.hora_inicio = starting_time
        self.hora_fin = ending_time

    @classmethod
    async def from_request(cls, request: Request, is_new: bool) -> object:
        data = await request.json()
        return Turnos(
            data.get("id"),
            data.get("hora_inicio"),
            data.get("hora_fin"),
            is_new,
        )

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [
            Turnos(row["id"], row["hora_inicio"], row["hora_fin"], False)
            for row in result
        ]

    @classmethod
    def get_row(cls, prim_keys: dict) -> None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(result["id"], result["hora_inicio"], result["hora_fin"], False)

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.id) is not int:
            return False

        if type(self.hora_inicio) is not time:
            return False

        if type(self.hora_fin) is not time:
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            return connection.insert_row(
                self.table,
                self.to_dict(),
            )
        else:
            return connection.update_row(
                self.table,
                self.to_dict(),
                {"id": self.id},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"id": self.id}):
            self.id = None
            self.hora_inicio = None
            self.hora_fin = None
