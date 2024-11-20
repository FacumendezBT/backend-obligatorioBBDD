from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import jwt

from utils.token import SECRET_KEY
from utils.token import ALGORITHM

EXCLUDED_PATHS = ["/api/users/login", "/docs", "/openapi.json"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if "Authorization" not in request.headers:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        auth_header = request.headers["Authorization"]
        token = auth_header.split(" ")[1]  # Quita el "Bearer " del inicio

        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
