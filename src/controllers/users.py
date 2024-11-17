from base_controller.base_controller import BaseController, HTTPException
from fastapi import APIRouter, Request
from models.login import Login
from config.logger import app_logger as logger
from utils.token import create_access_token

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_users() -> list[dict]:
    return controller.get_all(Login)


@router.get("/{email}")
def get_user_by_email(email: str) -> dict:
    return controller.get_by_primkeys(Login, {"correo": email})


@router.post("/")
async def create_user(request: Request) -> bool:
    return await controller.create_from_request(Login, request)


@router.post("/login")
async def validate_user(request: Request) -> dict:
    err = "Invalid credentials."
    creds = await request.json()
    user = controller.get_by_primkeys(Login, {"correo": creds.get("correo")})

    try:
        if creds.get("contrasena") != user.get("contrasena"):
            raise HTTPException(status_code=401, detail=err)

        access_token = create_access_token(
            data={"correo": user.get("correo"), "admin": user.get("admin")}
        )
        return {
            "correo": user.get("correo"),
            "admin": user.get("admin"),
            "token": access_token,
        }

    except HTTPException as http_exec:
        logger.warning(f"HTTP {err}: {http_exec.detail}")
        raise http_exec


@router.put("/")
async def update_user(request: Request) -> bool:
    return await controller.update_from_request(Login, request)


@router.delete("/{email}")
def delete_alumno(email: str) -> bool:
    return controller.delete_from_primkeys(Login, {"correo": email})
