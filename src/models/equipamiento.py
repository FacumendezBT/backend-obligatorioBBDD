from models.generic_model import GenericModel
from db import ConnectionSingleton


class Equipamiento(GenericModel):
    table: str = "equipamiento"
    id: int
    id_actividad: int
    descripcion: str
    costo: int
    is_new: bool

    def __init__(
        self, id: int, id_actividad: int, descripcion: str, costo: int, is_new: bool
    ) -> None:
        self.id = id
        self.id_actividad = id_actividad
        self.descripcion = descripcion
        self.costo = costo
        self.is_new = is_new

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table)

        if not result:
            return []

        return [
            Equipamiento(
                row["id"],
                row["id_actividad"],
                row["descripcion"],
                row["costo"],
                False,
            )
            for row in result
        ]

    @classmethod
    def get_row(cls, prim_keys: dict) -> None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(
            result["id"],
            result["id_actividad"],
            result["descripcion"],
            result["costo"],
            False,
        )

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.id) is not int:
            return False

        if type(self.id_actividad) is not int:
            return False

        if type(self.descripcion) is not str:
            return False

        if type(self.costo) is not int:
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            connection.insert_row(
                self.table,
                {
                    "id": self.id,
                    "id_actividad": self.id_actividad,
                    "descripcion": self.descripcion,
                    "costo": self.costo,
                },
            )
        else:
            connection.update_row(
                self.table,
                {
                    "id": self.id,
                    "id_actividad": self.id_actividad,
                    "descripcion": self.descripcion,
                    "costo": self.costo,
                },
                {"id": self.id},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"id": self.id}):
            self.id = None
            self.id_actividad = None
            self.descripcion = None
            self.costo = None
