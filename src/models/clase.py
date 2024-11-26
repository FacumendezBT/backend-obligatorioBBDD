from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection
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
        self,
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
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("id"),
            request_data.get("ci_instructor"),
            request_data.get("id_actividad"),
            request_data.get("id_turno"),
            request_data.get("dictada"),
            request_data.get("fecha"),
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
    def get_row(cls, prim_keys: dict) -> object | None:
        db = DatabaseConnection()
        result = db.get_row(cls.table, prim_keys)

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
        # Validaciones básicas
        if not isinstance(self.ci_instructor, int):
            return False

        if not isinstance(self.id_actividad, int):
            return False

        if not isinstance(self.id_turno, int):
            return False

        if not isinstance(self.dictada, bool):
            return False

        if not isinstance(self.fecha, date):
            return False

        db = DatabaseConnection()
        if self.is_new:
            success = db.insert_row(
                self.table,
                self.to_dict(),
            )
        else:
            if not isinstance(self.id, int):
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
            self.ci_instructor = None
            self.id_actividad = None
            self.id_turno = None
            self.dictada = None
            self.fecha = None
        return success
