from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.actividad import Actividad

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_actividades() -> list[dict]:
    return controller.get_all(Actividad)


@router.get("/{id}")
def get_actividad_by_id(id: int) -> dict:
    return controller.get_by_primkeys(Actividad, {"id": id})


@router.post("/")
async def create_actividad(request: Request) -> bool:
    return await controller.create_from_request(Actividad, request)


@router.put("/")
async def update_actividad(request: Request) -> bool:
    return await controller.update_from_request(Actividad, request)


@router.delete("/{id}")
def delete_actividad(id: int) -> bool:
    return controller.delete_from_primkeys(Actividad, {"id": id})
