"""
Description: This class represents a tuple of the login(...) table in the database.
"""

from models.generic_model import GenericModel


class Login(GenericModel):
    table = "login"

    def __init__(self, mail: str, password: str) -> None:
        super.__init__()
        self.correo = mail
        self.contrasena = password

    def insert_row(self, row: dict):
        # TODO hacer chequeos de la entrada

        super().insert_row(row)

    @classmethod
    def map_result(cls: object, result_row: dict) -> object:
        return cls(result_row["correo"], result_row["contrasena"])
