from models.generic_model import GenericModel
from db.database_connection import DatabaseConnection
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
        descripcion: str,
        costo: int,
        restricion_edad: int,
        is_new: bool,
    ) -> None:
        self.id = id
        self.descripcion = descripcion
        self.costo = costo
        self.restricion_edad = restricion_edad
        self.is_new = is_new

    @classmethod
    def from_request(cls, request_data: dict, is_new: bool) -> object:
        return cls(
            request_data.get("id"),
            request_data.get("descripcion"),
            request_data.get("costo"),
            request_data.get("restricion_edad"),
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
                row["descripcion"],
                row["costo"],
                row["restricion_edad"],
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
            result["descripcion"],
            result["costo"],
            result["restricion_edad"],
            False,
        )

    def save(self) -> bool:
        # Validaciones básicas
        if not isinstance(self.id, int): 
            return False
        if not isinstance(self.descripcion, str): 
            return False
        if not isinstance(self.costo, int): 
            return False
        if not isinstance(self.restricion_edad, int): 
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
                {"id": self.id},
            )
        return success
        
    def delete_self(self) -> bool:
        db = DatabaseConnection()
        success = db.delete_row(self.table, {"id": self.id})
        if success:
            self.id = None
            self.descripcion = None
            self.costo = None
            self.restricion_edad = None
        return success
