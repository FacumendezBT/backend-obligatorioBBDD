from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse


EXCLUDED_PATHS = ["/api/usuarios/login", "/docs", "/openapi.json"]


class AdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if request.method == "GET":
            return await call_next(request)

        if request.state.user.get("admin") != 1:
            return JSONResponse(
                status_code=401, content="Administrator rights are needed."
            )

        return await call_next(request)
