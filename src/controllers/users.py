from base_controller.base_controller import BaseController, HTTPException
from fastapi import APIRouter, Request
from models.login import Login
from config.logger import app_logger as logger
from utils.token import create_access_token

router = APIRouter()
controller = BaseController()


@router.get("/", summary="Obtener todos los usuarios",
    responses={
        200: {
            "description": "Lista de usuarios obtenida exitosamente.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "correo": "user1@example.com",
                            "contrasena": "hashed_password_1",
                            "admin": False
                        },
                        {
                            "correo": "admin@example.com",
                            "contrasena": "hashed_password_2",
                            "admin": True
                        }
                    ]
                }
            }
        }
    }
)
def get_all_users() -> list[dict]:
    """
    Obtener todos los usuarios registrados en el sistema.
    """
    return controller.get_all(Login)


@router.get("/{email}", summary="Obtener un usuario por correo",
    responses={
        200: {
            "description": "Usuario obtenido exitosamente.",
            "content": {
                "application/json": {
                    "example": {
                        "correo": "user1@example.com",
                        "contrasena": "hashed_password_1",
                        "admin": False
                    }
                }
            }
        },
        404: {"description": "Usuario no encontrado."}
    }
)
def get_user_by_email(email: str) -> dict:
    """
    Obtener un usuario específico por su correo electrónico.
    """
    return controller.get_by_primkeys(Login, {"correo": email})


@router.post("/", summary="Registrar un nuevo usuario",
    responses={
        201: {"description": "Usuario creado exitosamente."},
        400: {"description": "Datos inválidos."}
    }
)
async def create_user(request: Request) -> bool:
    """
    Registrar un nuevo usuario en el sistema.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "correo": "new_user@example.com",
          "contrasena": "hashed_password",
          "admin": false
      }
      ```
    """
    return await controller.create_from_request(Login, request)


@router.post("/login", summary="Validar credenciales de usuario",
    responses={
        200: {
            "description": "Credenciales válidas. Token de acceso generado.",
            "content": {
                "application/json": {
                    "example": {
                        "correo": "user1@example.com",
                        "admin": False,
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            }
        },
        401: {"description": "Credenciales inválidas."}
    }
)
async def validate_user(request: Request) -> dict:
    """
    Validar las credenciales de inicio de sesión y generar un token de acceso.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "correo": "user1@example.com",
          "contrasena": "hashed_password"
      }
      ```

    - **Respuesta exitosa**:
      ```json
      {
          "correo": "user1@example.com",
          "admin": false,
          "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      }
      ```
    """
    err = "Invalid credentials."
    creds = await request.json()
    user = controller.get_by_primkeys(Login, {"correo": creds.get("correo")})

    try:
        if creds.get("contrasena") != user.get("contrasena"):
            raise HTTPException(status_code=401, detail=err)

        access_token = create_access_token(
            data={"correo": user.get("correo"), "admin": user.get("admin")}
        )
        return {
            "correo": user.get("correo"),
            "admin": user.get("admin"),
            "token": access_token,
        }

    except HTTPException as http_exec:
        logger.warning(f"HTTP {err}: {http_exec.detail}")
        raise http_exec


@router.put("/", summary="Actualizar un usuario existente",
    responses={
        200: {"description": "Usuario actualizado exitosamente."},
        400: {"description": "Datos inválidos."},
        404: {"description": "Usuario no encontrado."}
    }
)
async def update_user(request: Request) -> bool:
    """
    Actualizar un usuario existente en el sistema.

    - **Cuerpo de la solicitud**:
      ```json
      {
          "correo": "user1@example.com",
          "contrasena": "new_hashed_password",
          "admin": false
      }
      ```
    """
    return await controller.update_from_request(Login, request)


@router.delete("/{email}", summary="Eliminar un usuario",
    responses={
        200: {"description": "Usuario eliminado exitosamente."},
        404: {"description": "Usuario no encontrado."}
    }
)
def delete_user(email: str) -> bool:
    """
    Eliminar un usuario específico por su correo electrónico.
    """
    return controller.delete_from_primkeys(Login, {"correo": email})
