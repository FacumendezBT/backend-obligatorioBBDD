from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.alumno import Alumno
from models.alumno_clase import AlumnoClase

router = APIRouter()
controller = BaseController()


@router.get("/")
def get_all_alumnos() -> list[dict]:
    return controller.get_all(Alumno)


@router.get("/{ci}")
def get_alumno_by_id(ci: int) -> dict:
    return controller.get_by_primkeys(Alumno, {"ci": ci})

@router.get("/{ci}/clases")
def get_clases_of_alumno(ci: int) -> list:
    return controller.get_by_attr(AlumnoClase, {"ci_alumno": ci})


@router.post("/")
async def create_alumno(request: Request) -> bool:
    return await controller.create_from_request(Alumno, request)


@router.put("/")
async def update_alumno(request: Request) -> bool:
    return await controller.update_from_request(Alumno, request)


@router.delete("/{ci}")
def delete_alumno(ci: int) -> bool:
    return controller.delete_from_primkeys(Alumno, {"ci": ci})
