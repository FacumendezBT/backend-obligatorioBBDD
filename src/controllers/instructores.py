from src.db.connection import Connection
from src.pydantics.instructores import Instructor
from fastapi import HTTPException


"""
Description: 
    This function is responsible for obtaining all the instructors from the database.

Returns:
    List[Instructor]: A list of Instructor objects, each representing an instructor.
"""
def get_instructores() -> list[Instructor]:
    try:
        bd_connection = Connection()
        consulta = "SELECT ci, nombre, apellido FROM instructor"
        result = bd_connection.run_query(consulta)
        bd_connection.end_connection()

        if isinstance(result, Exception):
            raise result

        instructores = [Instructor(**instructor) for instructor in result]
        return instructores
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting instructors, what a year!") from e