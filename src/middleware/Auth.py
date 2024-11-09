import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

SECRET_KEY = "eleze"
ALGORITHM = "HS256"  # Algoritmo de codificación
def verify_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        auth_header = request.headers["Authorization"]
        token = auth_header.split(" ")[1]  # Quita el "Bearer " del inicio
        verify_jwt_token(token)  # Verifica el token
        response = await call_next(request)
        return response
