from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.equipamiento import Equipamiento

router = APIRouter()
controller = BaseController()


@router.get("/", summary="Obtener todo el equipamiento",
    responses={
        200: {
            "description": "Equipamiento obtenido exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "id_actividad": 1,
                            "descripcion": "Casco de esquí",
                            "costo": 50
                        },
                        {
                            "id": 2,
                            "id_actividad": 2,
                            "descripcion": "Tabla de snowboard",
                            "costo": 150
                        }
                    ]
                }
            }
        }
    }
)
def get_all_equipamiento() -> list[dict]:
    """
    Obtener una lista de todo el equipamiento disponible.
    """
    return controller.get_all(Equipamiento)


@router.get("/{id}", summary="Obtener equipamiento por ID",
    responses={
        200: {
            "description": "Equipamiento obtenido exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "id_actividad": 1,
                        "descripcion": "Casco de esquí",
                        "costo": 50
                    }
                }
            }
        },
        404: {"description": "Equipamiento no encontrado."}
    }
)
def get_equipamiento_by_id(id: int) -> dict:
    """
    Obtener información detallada de un equipamiento específico por su ID.
    """
    return controller.get_by_primkeys(Equipamiento, {"id": id})


@router.post("/", summary="Crear nuevo equipamiento",
    responses={
        201: {
            "description": "Equipamiento creado exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "id_actividad": 1,
                        "descripcion": "Guantes térmicos",
                        "costo": 25
                    }
                }
            }
        },
        400: {"description": "Datos inválidos."}
    }
)
async def create_equipamiento(request: Request) -> bool:
    """
    Crear un nuevo equipamiento.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "id_actividad": 1,
          "descripcion": "Guantes térmicos",
          "costo": 25
      }
      ```
    """
    return await controller.create_from_request(Equipamiento, request)


@router.put("/", summary="Actualizar equipamiento existente",
    responses={
        200: {
            "description": "Equipamiento actualizado exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "id_actividad": 1,
                        "descripcion": "Casco de esquí reforzado",
                        "costo": 60
                    }
                }
            }
        },
        400: {"description": "Datos inválidos."},
        404: {"description": "Equipamiento no encontrado."}
    }
)
async def update_equipamiento(request: Request) -> bool:
    """
    Actualizar información de un equipamiento existente.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "id": 1,
          "id_actividad": 1,
          "descripcion": "Casco de esquí reforzado",
          "costo": 60
      }
      ```
    """
    return await controller.update_from_request(Equipamiento, request)


@router.delete("/{id}", summary="Eliminar equipamiento",
    responses={
        200: {"description": "Equipamiento eliminado exitosamente."},
        404: {"description": "Equipamiento no encontrado."}
    }
)
def delete_equipamiento(id: int) -> bool:
    """
    Eliminar un equipamiento específico por su ID.
    """
    return controller.delete_from_primkeys(Equipamiento, {"id": id})
