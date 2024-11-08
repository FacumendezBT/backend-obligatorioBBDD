from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton


class Instructor(GenericModel):
    table: str = "instructor"
    ci: int
    nombre: str
    apellido: str
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "ci": self.ci,
            "nombre": self.nombre,
            "apellido": self.apellido,
        }

    def __init__(
        self, ci: int, nombre: str, apellido: str, is_new: bool
    ) -> None:
        super().__init__()
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
        self.is_new = is_new
    

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [
            Instructor(row["ci"], row["nombre"], row["apellido"], False)
            for row in result
        ]

    @classmethod
    def get_row(cls, prim_keys: dict) -> None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(result["ci"], result["nombre"], result["apellido"], False)

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.ci) is not int:
            return False

        if type(self.nombre) is not str:
            return False

        if type(self.apellido) is not str:
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            connection.insert_row(
                self.table,
                self.to_dict()
            )
        else:
            connection.update_row(
                self.table,
                self.to_dict(),
                {"ci": self.ci},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"ci": self.ci}):
            self.ci = None
            self.nombre = None
            self.apellido = None
