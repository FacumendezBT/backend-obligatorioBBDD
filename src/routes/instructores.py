from typing import List
from fastapi import APIRouter, HTTPException
from src.pydantic.instructores import Instructor
from src.controllers.instructores import get_instructores

PREFIX = "/instructores"
router = APIRouter()


@router.get(PREFIX, response_model=List[Instructor])
def get_instructores():
    return get_instructores()
