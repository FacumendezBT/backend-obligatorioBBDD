from pydantic import BaseModel
from pydantic.v1 import validator
from src.utils.ci_validator import CIValidator

"""
Description: This 
"""
class InstructorBase(BaseModel):
    nombre: str
    apellido: str

class InstructorCreate(InstructorBase):
    ci: int

    @validator('ci')
    def ci_valid(cls, v):
        if not CIValidator.is_valid(v):
            raise ValueError('CI inválido')
        return v


class Instructor(InstructorBase):
    ci: int
