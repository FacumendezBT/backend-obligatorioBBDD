from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse


EXCLUDED_PATHS = ["/api/usuarios/login", "/docs", "/openapi.json"]


class AdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        print("pasamos por admin")
        print("Request Headers:", request.headers)
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if request.state.user.get("admin") != 1:
            return JSONResponse(
                status_code=401, content="Administrator rights are needed."
            )

        print("Request Headers:", request.headers)
        return await call_next(request)
