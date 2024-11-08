from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton
from datetime import date


class Clase(GenericModel):
    table: str = "clase"
    id: int
    ci_instructor: int
    id_actividad: int
    id_turno: int
    dictada: bool
    fecha: date
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ci_instructor": self.ci_instructor,
            "id_actividad": self.id_actividad,
            "id_turno": self.id_turno,
            "dictada": self.dictada,
            "fecha": self.fecha,
        }

    def __init__(
        self: object,
        id: int,
        ci_instructor: int,
        id_actividad: int,
        id_turno: int,
        dictada: bool,
        fecha: date,
        is_new: bool,
    ) -> None:
        self.id = id
        self.ci_instructor = ci_instructor
        self.id_actividad = id_actividad
        self.id_turno = id_turno
        self.dictada = dictada
        self.fecha = fecha
        self.is_new = is_new

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [
            Clase(
                row["id"],
                row["ci_instructor"],
                row["id_actividad"],
                row["id_turno"],
                row["dictada"],
                row["fecha"],
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
            result["ci_instructor"],
            result["id_actividad"],
            result["id_turno"],
            result["dictada"],
            result["fecha"],
            False,
        )

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.id) is not int:
            return False

        if type(self.ci_instructor) is not int:
            return False

        if type(self.id_actividad) is not int:
            return False

        if type(self.id_turno) is not int:
            return False

        if type(self.dictada) is not bool:
            return False

        if type(self.fecha) is not date:
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            connection.insert_row(
                self.table,
                self.to_dict(),
            )
        else:
            connection.update_row(
                self.table,
                self.to_dict(),
                {"id": self.id},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"id": self.id}):
            self.id = None
            self.ci_instructor = None
            self.id_actividad = None
            self.id_turno = None
            self.dictada = None
            self.fecha = None
