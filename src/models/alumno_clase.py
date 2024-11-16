from models.generic_model import GenericModel
from db.connection_singleton import ConnectionSingleton


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
    def from_request(self, request_data: dict, is_new: bool) -> object:
        return AlumnoClase(
            request_data.get("id_clase"),
            request_data.get("ci_alumno"),
            request_data.get("id_equipamiento"),
            is_new,
        )

    @classmethod
    def get_all(cls) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all(cls.table)

        if not result:
            return []

        return [
            AlumnoClase(
                row["id_clase"], row["ci_alumno"], row["id_equipamiento"], False
            )
            for row in result
        ]

    @classmethod
    def get_all_with(cls, attributes: dict) -> list[object]:
        connection = ConnectionSingleton().get_instance()
        result: dict = connection.get_all_with(cls.table, attributes)

        if not result:
            return []

        return [
            AlumnoClase(
                row["id_clase"], row["ci_alumno"], row["id_equipamiento"], False
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
            result["id_clase"], result["ci_alumno"], result["id_equipamiento"], False
        )

    def save(self) -> bool:
        # Chequeo bien bobo
        if type(self.id_clase) is not int:
            return False

        if type(self.ci_alumno) is not int:
            return False

        if type(self.id_equipamiento) is not int:
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
                {"id_clase": self.id_clase, "ci_alumno": self.ci_alumno},
            )

    def delete_self(self) -> bool:
        connection = ConnectionSingleton().get_instance()
        if connection.delete_row(
            self.table, {"id_clase": self.id_clase, "ci_alumno": self.ci_alumno}
        ):
            self.id_clase = None
            self.ci_alumno = None
            self.id_equipamiento = None
