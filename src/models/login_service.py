from jose import jwt
from datetime import datetime, timedelta
# from config import db_config
from db.connection_singleton import ConnectionSingleton
import os

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "eleze")
ALGORITHM = "HS256"
Token_Expire_Days = 30


class LoginService:
    def __init__(self):
        # Obtener instancia del singleton
        self.db = ConnectionSingleton.get_instance()

    def authenticate_user(self, email: str, password: str) -> dict | None:
        # Autentica al usuario y, si es válido, genera un token JWT.
        user = self.get_user_by_email(email)

        if not user or user["password"] != password:
            return None

        access_token = self.create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}

    def get_user_by_email(self, email: str) -> dict | None:
        # Usa el singleton para ejecutar la consulta
        result = self.db.get_row("users", {"email": email})

        return result  # Devuelve el usuario encontrado o None si no existe

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=Token_Expire_Days)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
