from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
import jwt

from utils.token import SECRET_KEY
from utils.token import ALGORITHM


EXCLUDED_PATHS = ["/api/usuarios/login", "/docs", "/openapi.json"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if "Authorization" not in request.headers:
            return JSONResponse(status_code=401, content="Authorization header missing")

        auth_header = request.headers["Authorization"]
        token = auth_header.split(" ")[1]

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = decoded_token
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content="Token has expired")
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content="Invalid token")

        return await call_next(request)
