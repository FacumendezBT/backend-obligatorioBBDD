from datetime import date
from datetime import datetime
from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection


class Alumno(GenericModel):
    table: str = "alumno"
    ci: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono_contacto: int
    correo_electronico: str
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "ci": self.ci,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "telefono_contacto": self.telefono_contacto,
            "correo_electronico": self.correo_electronico,
        }

    def __init__(
        self,
        ci: int,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        telefono_contacto: int,
        correo_electronico: str,
        is_new: bool,
    ) -> None:
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono_contacto = telefono_contacto
        self.correo_electronico = correo_electronico
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("ci"),
            request_data.get("nombre"),
            request_data.get("apellido"),
            request_data.get("fecha_nacimiento"),
            request_data.get("telefono_contacto"),
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
                row["fecha_nacimiento"],
                row["telefono_contacto"],
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
                row["fecha_nacimiento"],
                row["telefono_contacto"],
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
            result["fecha_nacimiento"],
            result["telefono_contacto"],
            result["correo_electronico"],
            False,
        )

    def guardar_datos(self):
        if isinstance(self.fecha_nacimiento, str):
            try:
                self.fecha_nacimiento = datetime.strptime(self.fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                print("Formato de fecha inválido")
                return False
        return True

    def save(self) -> bool:
        if not self.guardar_datos():
            return False
        if not isinstance(self.ci, int):
            return False
        if not isinstance(self.nombre, str):
            return False
        if not isinstance(self.apellido, str):
            return False
        if not isinstance(self.fecha_nacimiento, date):
            return False
        if not isinstance(self.telefono_contacto, str):
            return False
        if not isinstance(self.correo_electronico, str):
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
            self.fecha_nacimiento = None
            self.telefono_contacto = None
            self.correo_electronico = None
        return success
