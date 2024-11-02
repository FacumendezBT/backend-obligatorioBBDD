from datetime import date
from db import ConnectionSingleton
from models.generic_model import GenericModel


class Alumno:
    table: str = "alumno"
    ci: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono_contacto: int
    correo_electronico: str
    is_new: bool

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
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table)

        if not result:
            return []

        return [
            Alumno(
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
    def get_row(cls, prim_keys: dict) -> None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

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

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.ci) is not int:
            return False

        if type(self.nombre) is not str:
            return False

        if type(self.apellido) is not str:
            return False

        if type(self.fecha_nacimiento) is not date:
            return False

        if type(self.telefono_contacto) is not int:
            return False

        if type(self.correo_electronico) is not str:
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            connection.insert_row(
                self.table,
                {
                    "ci": self.ci,
                    "nombre": self.nombre,
                    "apellido": self.apellido,
                    "fecha_nacimiento": self.fecha_nacimiento,
                    "telefono_contacto": self.telefono_contacto,
                    "correo_electronico": self.correo_electronico,
                },
            )
        else:
            connection.update_row(
                self.table,
                {
                    "ci": self.ci,
                    "nombre": self.nombre,
                    "apellido": self.apellido,
                    "fecha_nacimiento": self.fecha_nacimiento,
                    "telefono_contacto": self.telefono_contacto,
                    "correo_electronico": self.correo_electronico,
                },
                {"ci": self.ci},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"ci": self.ci}):
            self.ci = None
            self.nombre = None
            self.apellido = None
            self.fecha_nacimiento = None
            self.telefono_contacto = None
            self.correo_electronico = None
