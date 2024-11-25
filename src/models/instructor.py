from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection


class Instructor(GenericModel):
    table: str = "instructor"
    ci: int
    nombre: str
    apellido: str
    correo_electronico: str
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "ci": self.ci,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo_electronico": self.correo_electronico,
        }

    def __init__(
        self, ci: int, nombre: str, apellido: str, correo_electronico: str, is_new: bool
    ) -> None:
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.correo_electronico = correo_electronico
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("ci"),
            request_data.get("nombre"),
            request_data.get("apellido"),
            request_data.get("correo_electronico"),
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
                row["ci"],
                row["nombre"],
                row["apellido"],
                row["correo_electronico"],
                False,
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
                row["ci"],
                row["nombre"],
                row["apellido"],
                row["correo_electronico"],
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
            result["ci"],
            result["nombre"],
            result["apellido"],
            result["correo_electronico"],
            False,
        )

    def save(self) -> bool:
        # Validaciones básicas
        if not isinstance(self.ci, int):
            return False

        if not isinstance(self.nombre, str):
            return False

        if not isinstance(self.apellido, str):
            return False

        if not isinstance(self.correo_electronico, str):
            return False

        db = DatabaseConnection()
        if self.is_new:
            success = db.insert_row(self.table, self.to_dict())
        else:
            success = db.update_row(
                self.table,
                self.to_dict(),
                {"ci": self.ci},
            )
        return success

    def delete_self(self) -> bool:
        db = DatabaseConnection()
        success = db.delete_row(self.table, {"ci": self.ci})
        if success:
            self.ci = None
            self.nombre = None
            self.apellido = None
            self.correo_electronico = None
        return success
