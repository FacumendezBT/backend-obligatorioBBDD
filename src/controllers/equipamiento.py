from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.equipamiento import Equipamiento

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_equipamiento() -> list[dict]:
    return controller.get_all(Equipamiento)


@router.get("/{id}")
def get_equipamiento_by_id(id: int) -> dict:
    return controller.get_by_primkeys(Equipamiento, {"id": id})


@router.post("/")
async def create_equipamiento(request: Request) -> bool:
    return await controller.create_from_request(Equipamiento, request)


@router.put("/")
async def update_equipamiento(request: Request) -> bool:
    return await controller.update_from_request(Equipamiento, request)


@router.delete("/{id}")
def delete_equipamiento(id: int) -> bool:
    return controller.delete_from_primkeys(Equipamiento, {"id": id})
