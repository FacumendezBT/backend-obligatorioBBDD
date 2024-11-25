from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.clase import Clase
from models.alumno_clase import AlumnoClase

router = APIRouter()
controller = BaseController()

@router.get("/", summary="Obtener todas las clases",
    responses={
        200: {
            "description": "Clases obtenidas exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "ci_instructor": 12345678,
                            "id_actividad": 1,
                            "id_turno": 2,
                            "dictada": True,
                            "fecha": "2024-11-01"
                        },
                        {
                            "id": 2,
                            "ci_instructor": 87654321,
                            "id_actividad": 2,
                            "id_turno": 3,
                            "dictada": False,
                            "fecha": "2024-11-05"
                        }
                    ]
                }
            }
        }
    }
)
def get_all_clases() -> list[dict]:
    """
    Obtener una lista de todas las clases disponibles.
    """
    return controller.get_all(Clase)


@router.get("/{id}", summary="Obtener una clase por ID",
    responses={
        200: {
            "description": "Clase obtenida exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "ci_instructor": 12345678,
                        "id_actividad": 1,
                        "id_turno": 2,
                        "dictada": True,
                        "fecha": "2024-11-01"
                    }
                }
            }
        },
        404: {"description": "Clase no encontrada."}
    }
)
def get_clase_by_id(id: int) -> dict:
    """
    Obtener información detallada de una clase específica por su ID.
    """
    return controller.get_by_primkeys(Clase, {"id": id})


@router.get("/{id}/alumnos", summary="Obtener alumnos de una clase",
    responses={
        200: {
            "description": "Lista de alumnos obtenida exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id_clase": 1,
                            "ci_alumno": 123456,
                            "id_equipamiento": 5
                        },
                        {
                            "id_clase": 1,
                            "ci_alumno": 654321,
                            "id_equipamiento": 3
                        }
                    ]
                }
            }
        },
        404: {"description": "Clase no encontrada."}
    }
)
def get_alumnos_of_clase(id: int) -> list:
    """
    Obtener la lista de alumnos registrados en una clase específica.
    """
    return controller.get_by_attr(AlumnoClase, {"id_clase": id})


@router.post("/", summary="Crear una nueva clase")
async def create_clase(request: Request) -> bool:
    """
    Crear una nueva clase.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "ci_instructor": 12345678,
          "id_actividad": 1,
          "id_turno": 2,
          "dictada": false,
          "fecha": "2024-11-10"
      }
      ```
    """
    return await controller.create_from_request(Clase, request)


@router.put("/", summary="Actualizar una clase existente")
async def update_clase(request: Request) -> bool:
    """
    Actualizar una clase existente.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "id": 1,
          "ci_instructor": 12345678,
          "id_actividad": 1,
          "id_turno": 2,
          "dictada": true,
          "fecha": "2024-11-01"
      }
      ```
    """
    return await controller.update_from_request(Clase, request)


@router.delete("/{id}", summary="Eliminar una clase",
    responses={
        200: {"description": "Clase eliminada exitosamente."},
        404: {"description": "Clase no encontrada."}
    }
)
def delete_clase(id: int) -> bool:
    """
    Eliminar una clase específica por su ID.
    """
    return controller.delete_from_primkeys(Clase, {"id": id})
