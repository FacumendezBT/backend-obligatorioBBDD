from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton


class Login(GenericModel):
    table: str = "login"
    correo: str
    contrasena: str
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "correo": self.correo, 
            "contrasena": self.contrasena
        }

    def __init__(self, correo: str, contrasena: str, is_new: bool) -> None:
        super.__init__()
        self.correo = correo
        self.contrasena = contrasena
        self.is_new = is_new

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [Login(row["correo"], row["contrasena"], False) for row in result]

    @classmethod
    def get_row(cls, prim_keys: dict) -> object | None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(result["correo"], result["contrasena"], False)

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.correo) is not str and type(self.contrasena) is not str:
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            connection.insert_row(self.table, self.to_dict())
        else:
            connection.update_row(
                self.table,
                self.to_dict(),
                {"correo": self.correo},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"correo": self.correo}):
            self.correo = None
            self.contrasena = None
