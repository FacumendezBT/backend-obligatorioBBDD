from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.turnos import Turnos

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_turnos() -> list[dict]:
    return controller.get_all(Turnos)


@router.get("/{id}")
def get_turno_by_id(id: int) -> dict:
    return controller.get_by_primkeys(Turnos, {"id": id})


@router.post("/")
async def create_turno(request: Request) -> bool:
    return await controller.create_from_request(Turnos, request)


@router.put("/")
async def update_turno(request: Request) -> bool:
    return await controller.update_from_request(Turnos, request)


@router.delete("/{id}")
def delete_turno(id: int) -> bool:
    return controller.delete_from_primkeys(Turnos, {"id": id})
