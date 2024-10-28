from models.generic_model import GenericModel


class Login(GenericModel):
    table: str = "login"

    correo: str = None
    contrasena: str = None

    def __init__(self) -> None:
        super.__init__()

    def get_row(self, prim_keys: dict) -> None:
        super().get_row(prim_keys)
        result: dict = self.cursor.fetchone()

        if result:
            self.correo = result["correo"]
            self.contrasena = result["contrasena"]
        else:
            # Anulamos x si estuviéramos reutilizando una
            # misma instancia para hacer los select
            self.correo = None
            self.contrasena = None

    def insert_row(self, row: dict) -> bool:
        try:
            # Chequeo bien bobo
            if type(row["correo"]) is not str and type(row["contrasena"]) is not str:
                self.msg = "TYPE ERROR"
                return False

        except KeyError:
            self.msg = "INVALID ATTRIBUTES"
            return False

        return super().insert_row(row)
