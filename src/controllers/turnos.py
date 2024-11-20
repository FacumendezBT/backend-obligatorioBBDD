from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.turnos import Turnos

router = APIRouter()
controller = BaseController()


@router.get("/", summary="Obtener todos los turnos",
    responses={
        200: {
            "description": "Lista de turnos obtenida exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "id_actividad": 1,
                            "fecha": "2024-11-20",
                            "hora_inicio": "09:00",
                            "hora_fin": "10:00",
                            "disponible": True
                        },
                        {
                            "id": 2,
                            "id_actividad": 2,
                            "fecha": "2024-11-21",
                            "hora_inicio": "10:00",
                            "hora_fin": "11:30",
                            "disponible": False
                        }
                    ]
                }
            }
        }
    }
)
def get_all_turnos() -> list[dict]:
    """
    Obtener todos los turnos disponibles en la base de datos.
    """
    return controller.get_all(Turnos)


@router.get("/{id}", summary="Obtener un turno por ID",
    responses={
        200: {
            "description": "Turno obtenido exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "id_actividad": 1,
                        "fecha": "2024-11-20",
                        "hora_inicio": "09:00",
                        "hora_fin": "10:00",
                        "disponible": True
                    }
                }
            }
        },
        404: {"description": "Turno no encontrado."}
    }
)
def get_turno_by_id(id: int) -> dict:
    """
    Obtener un turno específico por su ID.
    """
    return controller.get_by_primkeys(Turnos, {"id": id})


@router.post("/", summary="Crear un nuevo turno",
    responses={
        201: {
            "description": "Turno creado exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "id_actividad": 1,
                        "fecha": "2024-11-22",
                        "hora_inicio": "11:00",
                        "hora_fin": "12:00",
                        "disponible": True
                    }
                }
            }
        },
        400: {"description": "Datos inválidos."}
    }
)
async def create_turno(request: Request) -> bool:
    """
    Crear un nuevo turno.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "id_actividad": 1,
          "fecha": "2024-11-22",
          "hora_inicio": "11:00",
          "hora_fin": "12:00",
          "disponible": true
      }
      ```
    """
    return await controller.create_from_request(Turnos, request)


@router.put("/", summary="Actualizar un turno existente",
    responses={
        200: {
            "description": "Turno actualizado exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "id_actividad": 1,
                        "fecha": "2024-11-20",
                        "hora_inicio": "09:00",
                        "hora_fin": "10:30",
                        "disponible": True
                    }
                }
            }
        },
        400: {"description": "Datos inválidos."},
        404: {"description": "Turno no encontrado."}
    }
)
async def update_turno(request: Request) -> bool:
    """
    Actualizar un turno existente.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "id": 1,
          "id_actividad": 1,
          "fecha": "2024-11-20",
          "hora_inicio": "09:00",
          "hora_fin": "10:30",
          "disponible": true
      }
      ```
    """
    return await controller.update_from_request(Turnos, request)


@router.delete("/{id}", summary="Eliminar un turno",
    responses={
        200: {"description": "Turno eliminado exitosamente."},
        404: {"description": "Turno no encontrado."}
    }
)
def delete_turno(id: int) -> bool:
    """
    Eliminar un turno específico por su ID.
    """
    return controller.delete_from_primkeys(Turnos, {"id": id})
