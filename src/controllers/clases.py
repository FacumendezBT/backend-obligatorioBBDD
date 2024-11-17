from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.clase import Clase
from models.alumno_clase import AlumnoClase

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_clases() -> list[dict]:
    return controller.get_all(Clase)


@router.get("/{id}")
def get_clase_by_id(id: int) -> dict:
    return controller.get_by_primkeys(Clase, {"id": id})


@router.get("/{id}/alumnos")
def get_alumnos_of_clase(id: int) -> list:
    return controller.get_by_attr(AlumnoClase, {"id_clase": id})


@router.post("/")
async def create_clase(request: Request) -> bool:
    return await controller.create_from_request(Clase, request)


@router.put("/")
async def update_clase(request: Request) -> bool:
    return await controller.update_from_request(Clase, request)


@router.delete("/{id}")
def delete_clase(id: int) -> bool:
    return controller.delete_from_primkeys(Clase, {"id": id})
