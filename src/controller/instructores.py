from config.logger import app_logger as logger
from fastapi import HTTPException, Request
from models.instructor import Instructor


def get_all_instructores() -> list[dict]:
    try:
        instructores = Instructor.get_all()
        return [instructor.to_dict() for instructor in instructores]
    except Exception as e:
        logger.error(f"Error al obtener los instructores: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los instructores")

def get_instructor_by_id(ci: int) -> dict:
    try:
        instructor = Instructor.get_row({"ci": ci})
        if(instructor is None):
            raise HTTPException(status_code=404, detail="Instructor no encontrado")
        return instructor.to_dict()
    except HTTPException as http_exc:
        logger.warning(f"HTTP error al obtener el instructor por id: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error al obtener el instructor por id: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al obtener el instructor por id")
    
async def create_instructor(request: Request) -> bool:
    try:    
        instructor = await Instructor.from_request(request, True)
        success = instructor.save()
        return success
    except Exception as e:
        logger.error(f"Error al crear el instructor: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al crear el instructor")
    
async def update_instructor(request: Request) -> bool:
    try:
        instructor = await Instructor.from_request(request, False)
        success = instructor.save()
        return success
    except Exception as e:
        logger.error(f"Error al actualizar el instructor: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al actualizar el instructor")
    
def delete_instructor(ci: int) -> bool:
    try:
        instructor = Instructor.get_row({"ci": ci})
        if(instructor is None):
            raise HTTPException(status_code=404, detail="Instructor no encontrado")
        success = instructor.delete_self()
        return success
    except HTTPException as http_exc:
        logger.warning(f"HTTP error al eliminar el instructor: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error al eliminar el instructor: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al eliminar el instructor")