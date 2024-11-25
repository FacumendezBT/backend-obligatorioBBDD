from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.actividad import Actividad

router = APIRouter()
controller = BaseController()

@router.get("/", summary="Obtener todas las actividades",
    responses={
        200: {
            "description": "Actividades obtenidas exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "descripcion": "Clases de esquí", "costo": 5000, "restriccion_edad": 12},
                        {"id": 2, "descripcion": "Clases de snowboard", "costo": 4500, "restriccion_edad": 10}
                    ]
                }
            }
        }
    }
)
def get_all_actividades() -> list[dict]:
    """
    Obtener una lista de todas las actividades disponibles.
    """
    return controller.get_all(Actividad)

@router.get("/{id}", summary="Obtener una actividad por ID",
    responses={
        200: {
            "description": "Actividad obtenida exitosamente.",
            "content": {
                "application/json": {
                    "example": {"id": 1, "descripcion": "Clases de esquí", "costo": 5000, "restriccion_edad": 12}
                }
            }
        },
        404: {"description": "Actividad no encontrada."}
    }
)
def get_actividad_by_id(id: int) -> dict:
    """
    Obtener información detallada de una actividad específica por su ID.
    """
    return controller.get_by_primkeys(Actividad, {"id": id})

@router.post("/", summary="Crear una nueva actividad")
async def create_actividad(request: Request) -> bool:
    """
    Crear una nueva actividad.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "descripcion": "Clases de esquí",
          "costo": 5000,
          "restriccion_edad": 12
      }
      ```
    """
    return await controller.create_from_request(Actividad, request)

@router.put("/", summary="Actualizar una actividad existente")
async def update_actividad(request: Request) -> bool:
    """
    Actualizar una actividad existente.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "id": 1,
          "descripcion": "Clases avanzadas de esquí",
          "costo": 6000,
          "restriccion_edad": 15
      }
      ```
    """
    return await controller.update_from_request(Actividad, request)

@router.delete("/{id}", summary="Eliminar una actividad",
    description="Elimina una actividad específica usando su ID.",
    responses={
        200: {"description": "Actividad eliminada exitosamente."},
        404: {"description": "Actividad no encontrada."}
    }
)
def delete_actividad(id: int) -> bool:
    """
    Eliminar una actividad específica por su ID.
    """
    return controller.delete_from_primkeys(Actividad, {"id": id})
