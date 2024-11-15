from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton


class Login(GenericModel):
    table: str = "login"
    correo: str
    contrasena: str
    admin: bool
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "correo": self.correo,
            "contrasena": self.contrasena,
            "admin": self.admin,
        }

    def __init__(self, correo: str, contrasena: str, admin: bool, is_new: bool) -> None:
        super.__init__()
        self.correo = correo
        self.contrasena = contrasena
        self.admin = admin
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return Login(
            request_data.get("correo"),
            request_data.get("contrasena"),
            request_data.get("admin"),
            is_new,
        )

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [
            Login(row["correo"], row["contrasena"], row["admin"], False)
            for row in result
        ]

    @classmethod
    def get_row(cls, prim_keys: dict) -> object | None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(result["correo"], result["contrasena"], result["admin"], False)

    def save(self) -> bool:
        # Chequeo bien bobo
        if (
            type(self.correo) is not str
            and type(self.contrasena) is not str
            and type(self.admin) is not bool
        ):
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            return connection.insert_row(self.table, self.to_dict())
        else:
            return connection.update_row(
                self.table,
                self.to_dict(),
                {"correo": self.correo},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"correo": self.correo}):
            self.correo = None
            self.contrasena = None
            self.admin = None
