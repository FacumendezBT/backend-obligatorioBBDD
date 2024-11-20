from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection

class AlumnoClase(GenericModel):
    table: str = "alumno_clase"
    id_clase: int
    ci_alumno: int
    id_equipamiento: int
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "id_clase": self.id_clase,
            "ci_alumno": self.ci_alumno,
            "id_equipamiento": self.id_equipamiento,
        }

    def __init__(
        self, id_clase: int, ci_alumno: int, id_equipamiento: int, is_new: bool
    ) -> None:
        self.id_clase = id_clase
        self.ci_alumno = ci_alumno
        self.id_equipamiento = id_equipamiento
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("id_clase"),
            request_data.get("ci_alumno"),
            request_data.get("id_equipamiento"),
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
                row["id_clase"], row["ci_alumno"], row["id_equipamiento"], False
            )
            for row in result
        ]

    @classmethod
    def get_all_with(cls, attributes: dict) -> list[object]:
        db = DatabaseConnection()
        result = db.get_all_with(cls.table, attributes)

        if not result:
            return []

        return [
            cls(
                row["id_clase"], row["ci_alumno"], row["id_equipamiento"], False
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
            result["id_clase"], result["ci_alumno"], result["id_equipamiento"], False
        )

    def save(self) -> bool:
        # Validaciones básicas
        if not isinstance(self.id_clase, int):
            return False

        if not isinstance(self.ci_alumno, int):
            return False

        if not isinstance(self.id_equipamiento, int):
            return False

        db = DatabaseConnection()
        if self.is_new:
            success = db.insert_row(
                self.table,
                self.to_dict(),
            )
        else:
            success = db.update_row(
                self.table,
                self.to_dict(),
                {"id_clase": self.id_clase, "ci_alumno": self.ci_alumno},
            )
        return success

    def delete_self(self) -> bool:
        db = DatabaseConnection()
        success = db.delete_row(
            self.table, {"id_clase": self.id_clase, "ci_alumno": self.ci_alumno}
        )
        if success:
            self.id_clase = None
            self.ci_alumno = None
            self.id_equipamiento = None
        return success
