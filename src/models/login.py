from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection


class Login(GenericModel):
    table: str = "login"
    correo: str
    contrasena: str
    admin: int
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "correo": self.correo,
            "contrasena": self.contrasena,
            "admin": self.admin,
        }

    def __init__(self, correo: str, contrasena: str, admin: int, is_new: bool) -> None:
        self.correo = correo
        self.contrasena = contrasena
        self.admin = admin
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("correo"),
            request_data.get("contrasena"),
            request_data.get("admin"),
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
                row["correo"],
                row["contrasena"],
                row["admin"],
                False
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
            result["correo"],
            result["contrasena"],
            result["admin"],
            False
        )

    def save(self) -> bool:
        # Validaciones básicas
        if (
            not isinstance(self.correo, str)
            or not isinstance(self.contrasena, str)
            or not isinstance(self.admin, int)
        ):
            return False

        db = DatabaseConnection()
        if self.is_new:
            success = db.insert_row(
                self.table,
                self.to_dict()
            )
        else:
            success = db.update_row(
                self.table,
                self.to_dict(),
                {"correo": self.correo},
            )
        return success

    def delete_self(self) -> bool:
        db = DatabaseConnection()
        success = db.delete_row(self.table, {"correo": self.correo})
        if success:
            self.correo = None
            self.contrasena = None
            self.admin = None
        return success
