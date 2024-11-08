from fastapi import HTTPException
from models.instructor import Instructor

def get_all_instructores() -> list[dict]:
    try:
        instructores = Instructor.get_all()
        return [instructor.to_dict() for instructor in instructores]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al obtener los instructores")

def get_instructor_by_id(ci: int) -> dict:
    try:
        instructor = Instructor.get_row({"ci": ci})
        return instructor.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener el instructor por id")
    
def create_instructor(ci: int, nombre: str, apellido: str) -> bool:
    try:
        instructor = Instructor(ci, nombre, apellido, True)
        return instructor.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el instructor")
    
def update_instructor(ci: int, nombre: str, apellido: str) -> bool:
    try:
        instructor = Instructor.get_row({"ci": ci})
        instructor.nombre = nombre
        instructor.apellido = apellido
        return instructor.save()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar el instructor")