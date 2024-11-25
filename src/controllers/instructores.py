from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.instructor import Instructor

router = APIRouter()
controller = BaseController()


@router.get(
    "/",
    summary="Obtener todos los instructores",
    description="Obtiene una lista de todos los instructores registrados.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {"ci": 12345678, "nombre": "Ezequiel", "apellido": "Gonzalez", "correo_electronico": "eze@eze.com"},
                        {"ci": 87654321, "nombre": "Facundo", "apellido": "Mendez", "correo_electronico": "facundo@facundo.com"}
                    ]
                }
            }
        }
    }
)
def get_all_instructores() -> list[dict]:
    return controller.get_all(Instructor)


@router.get(
    "/{ci}",
    summary="Obtener un instructor por CI",
    description="Obtiene los datos de un instructor específico usando su CI (Primary Key).",
    responses={
        200: {
            "description": "Instructor encontrado exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "ci": 12345678,
                        "nombre": "Ezequiel",
                        "apellido": "Gonzalez",
                        "correo_electronico": "eze@eze.com"
                    }
                }
            }
        }
    }
)
def get_instructor_by_id(ci: int) -> dict:
    return controller.get_by_primkeys(Instructor, {"ci": ci})

@router.post("/", summary="Crear un nuevo instructor")
async def create_instructor(request: Request) -> bool:
    """
    Crear un nuevo instructor.

    - **Cuerpo de la solicitud**:
      ```json
      {
          ci: int,
          nombre: string,
          apellido: string,
          correo_electronico: <EMAIL>
      }
      ```
    """
    return await controller.create_from_request(Instructor, request)


@router.put("/", summary="Actualizar un instructor")
async def update_instructor(request: Request) -> bool:
    """
    Actualizar un instructor.

    - **Cuerpo de la solicitud**:
      ```json
      {
          ci: int,
          nombre: string,
          apellido: string,
          correo_electronico: <EMAIL>
      }
"""
    return await controller.update_from_request(Instructor, request)


@router.delete("/{ci}", summary="Eliminar un instructor", description="Elimina un instructor específico usando su CI.")
def delete_instructor(ci: int) -> bool:
    return controller.delete_from_primkeys(Instructor, {"ci": ci})
