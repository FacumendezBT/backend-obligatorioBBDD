from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.login import Login

router = APIRouter()
controller = BaseController()

# Medio chancho tirar el mail x url
# Capaz que podemos codificarlo en el front y decodificarlo acá (?)
@router.get("/")
def get_all_users() -> list[dict]:
    return controller.get_all(Login)


@router.get("/{email}")
def get_user_by_email(email: str) -> dict:
    return controller.get_by_primkeys(Login, {"correo": email})


@router.post("/")
async def create_user(request: Request) -> bool:
    return await controller.create_from_request(Login, request)


@router.put("/")
async def update_user(request: Request) -> bool:
    return await controller.update_from_request(Login, request)


@router.delete("/{email}")
def delete_alumno(email: str) -> bool:
    return controller.delete_from_primkeys(Login, {"correo": email})
