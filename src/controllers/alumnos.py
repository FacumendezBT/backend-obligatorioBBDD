from base_controller.base_controller import BaseController
from fastapi import APIRouter, Request
from models.alumno import Alumno
from models.alumno_clase import AlumnoClase

router = APIRouter()
controller = BaseController()


@router.get("/", summary="Obtener alumnos",
    responses={
        200: {
            "description": "Lista de alumnos obtenida exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "ci": 12345678,
                            "nombre": "Ezequiel",
                            "apellido": "Gonzalez",
                            "fecha_nacimiento": "2001-03-24",
                            "telefono_contacto": "093365735",
                            "correo_electronico": "eze@eze.com"
                        },
                        {
                            "ci": 87654321,
                            "nombre": "Facundo",
                            "apellido": "Mendez",
                            "fecha_nacimiento": "2003-03-24",
                            "telefono_contacto": "093365999",
                            "correo_electronico": "facundo@facundo.com"
                        }
                    ]
                }
            }
        }
    }
)
def get_all_alumnos() -> list[dict]:
    """
    Obtener todos los alumnos registrados.
    """
    return controller.get_all(Alumno)


@router.get("/{ci}", summary="Obtener un alumno por CI",
    responses={
        200: {
            "description": "Alumno encontrado exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "ci": 12345678,
                        "nombre": "Ezequiel",
                        "apellido": "Gonzalez",
                        "fecha_nacimiento": "2001-03-24",
                        "telefono_contacto": "093365735",
                        "correo_electronico": "eze@eze.com"
                    }
                }
            }
        }
    }
)
def get_alumno_by_id(ci: int) -> dict:
    """
    Obtener un alumno específico utilizando su CI.
    """
    return controller.get_by_primkeys(Alumno, {"ci": ci})


@router.get("/{ci}/clases", summary="Obtener clases de un alumno",
    responses={
        200: {
            "description": "Clases del alumno obtenidas exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {"id_clase": 1, "ci_alumno": 32315234, "id_equipamiento": 3314253},
                        {"id_clase": 2, "ci_alumno": 52315234, "id_equipamiento": 5314253}
                    ]
                }
            }
        }
    }
)
def get_clases_of_alumno(ci: int) -> list:
    """
    Obtener todas las clases asociadas a un alumno específico utilizando su CI.
    """
    return controller.get_by_attr(AlumnoClase, {"ci_alumno": ci})


@router.post("/", summary="Crear un nuevo alumno")
async def create_alumno(request: Request) -> bool:
    """
    Crear un nuevo alumno.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "ci": int,
          "nombre": "string",
          "apellido": "string",
          "fecha_nacimiento": "YYYY-MM-DD",
          "telefono_contacto": "string",
          "correo_electronico": "string"
      }
      ```
    """
    return await controller.create_from_request(Alumno, request)


@router.put("/", summary="Actualizar un alumno")
async def update_alumno(request: Request) -> bool:
    """
    Actualizar un alumno existente.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "ci": int,
          "nombre": "string",
          "apellido": "string",
          "fecha_nacimiento": "YYYY-MM-DD",
          "telefono_contacto": "string",
          "correo_electronico": "string"
      }
      ```
    """
    return await controller.update_from_request(Alumno, request)


@router.delete("/{ci}", summary="Eliminar un alumno",
    description="Elimina un alumno específico utilizando su CI.",
    responses={
        200: {
            "description": "Alumno eliminado exitosamente."
        }
    }
)
def delete_alumno(ci: int) -> bool:
    """
    Eliminar un alumno específico utilizando su CI.
    """
    return controller.delete_from_primkeys(Alumno, {"ci": ci})