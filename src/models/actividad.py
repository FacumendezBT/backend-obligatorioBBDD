from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton


class Actividad(GenericModel):
    table: str = "actividad"
    id: int
    descripcion: str
    costo: int
    restricion_edad: int
    is_new: bool

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "costo": self.costo,
            "restricion_edad": self.restricion_edad,
        }

    def __init__(
        self,
        id: int,
        description: str,
        cost: int,
        age_restrict: int,
        is_new: bool,
    ) -> None:
        self.id = id
        self.descripcion = description
        self.costo = cost
        self.restricion_edad = age_restrict
        self.is_new = is_new

    @classmethod
    def from_request(self, request_data: dict, is_new: bool) -> object:
        return Actividad(
            request_data.get("id"),
            request_data.get("descripcion"),
            request_data.get("costo"),
            request_data.get("restricion_edad"),
            is_new,
        )
        
    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [
            Actividad(
                row["id"],
                row["descripcion"],
                row["costo"],
                row["restricion_edad"],
                False,
            )
            for row in result
        ]

    @classmethod
    def get_row(cls, prim_keys: dict) -> object | None:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_row(cls.table, prim_keys)

        if not result:
            return None

        return cls(
            result["id"],
            result["descripcion"],
            result["costo"],
            result["restricion_edad"],
            False,
        )

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.id) is not int: 
            return False

        if type(self.descripcion) is not str: 
            return False

        if type(self.costo) is not int: 
            return False

        if type(self.restricion_edad) is not int: 
            return False

        connection = ConnectionSingleton().get_instance()
        if self.is_new:
            return connection.insert_row(
                self.table,
                self.to_dict(),
            )
        else:
            return connection.update_row(
                self.table,
                self.to_dict(),
                {"id": self.id},
            )
        
    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(self.table, {"id": self.id}):
            self.id = None
            self.descripcion = None
            self.costo = None
            self.restricion_edad = None
